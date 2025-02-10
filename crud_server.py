import grpc
import crud_service_pb2
import crud_service_pb2_grpc

from concurrent import futures
import logging
import threading
import time

from nodes import NODES
from tabulate import tabulate

# Bộ nhớ lưu trữ dữ liệu của node (không có tính chất bền vững)
CLOUD_DB = {}

server_port = input("Choose a port to serve: ")

class CloudStorage(crud_service_pb2_grpc.CloudStorageServicer):
    def __init__(self):
        # Khởi tạo các neighbor (các node khác trong hệ thống)
        self.__neighbors = {}
        for port in NODES:
            if port != server_port:
                self.__neighbors[port] = {
                    'stub': crud_service_pb2_grpc.CloudStorageStub(
                        channel=grpc.insecure_channel(f"localhost:{port}")
                    ),
                    'alive': True
                }
        # Bắt đầu thread gửi heartbeat định kỳ để kiểm tra tình trạng các node láng giềng
        heartbeat_thread = threading.Thread(target=self.__heartbeat_loop, daemon=True)
        heartbeat_thread.start()

        # Sau một thời gian ngắn (để heartbeat có thể xác định trạng thái các neighbor),
        # nếu CLOUD_DB rỗng thì thực hiện khôi phục dữ liệu từ một node khác.
        # Phiên bản cập nhật: nếu recovery thất bại, sẽ thử lại theo chu kỳ.
        threading.Thread(target=self.__recover_data, daemon=True).start()

    # --- Các phương thức CRUD ---
    def Create(self, request, context):
        if request.key in CLOUD_DB.keys():
            return crud_service_pb2.Response(
                status_code=409, message=f"The key {request.key} is already exist!"
            )
        CLOUD_DB[request.key] = request.value
        self.__add_sync(request.key, request.value)
        self.__show()
        return crud_service_pb2.Response(
            status_code=200,
            message=f"The key-value pair {{{request.key}: {request.value}}} has been added successfully!",
        )

    def Read(self, request, context):
        if request.key not in CLOUD_DB.keys():
            return crud_service_pb2.Response(status_code=404, message="Key not found!")
        return crud_service_pb2.Response(
            status_code=200, message=f"{{{request.key}: {CLOUD_DB.get(request.key)}}}"
        )

    def Update(self, request, context):
        if request.key not in CLOUD_DB.keys():
            return crud_service_pb2.Response(status_code=404, message="Key not found!")
        if CLOUD_DB[request.key] != request.value:
            CLOUD_DB[request.key] = request.value
            self.__update_sync(request.key, request.value)
            self.__show()
        return crud_service_pb2.Response(
            status_code=200,
            message=f"The key-value pair {{{request.key}: {request.value}}} has been updated successfully!",
        )

    def Delete(self, request, context):
        if request.key not in CLOUD_DB.keys():
            return crud_service_pb2.Response(status_code=404, message="Key not found!")
        CLOUD_DB.pop(request.key)
        self.__delete_sync(request.key)
        self.__show()
        return crud_service_pb2.Response(
            status_code=200, message=f"Key {request.key} has been removed successfully!"
        )

    # --- RPC Heartbeat: cho phép các node khác kiểm tra tình trạng của node này ---
    def Heartbeat(self, request, context):
        return crud_service_pb2.Response(status_code=200, message="Alive")

    # --- RPC Snapshot: trả về toàn bộ dữ liệu của node ---
    def Snapshot(self, request, context):
        records = []
        for key, value in CLOUD_DB.items():
            records.append(crud_service_pb2.Record(key=key, value=value))
        return crud_service_pb2.SnapshotResponse(records=records)

    # --- Các phương thức đồng bộ dữ liệu với các node láng giềng ---
    def __add_sync(self, key, value):
        for port, neighbor in self.__neighbors.items():
            if neighbor['alive']:
                try:
                    neighbor['stub'].Create(crud_service_pb2.Record(key=key, value=value))
                except grpc.RpcError as e:
                    print(f"[SYNC-ERROR] Node at {port} is down during Create sync: {e}")
                    neighbor['alive'] = False

    def __update_sync(self, key, value):
        for port, neighbor in self.__neighbors.items():
            if neighbor['alive']:
                try:
                    neighbor['stub'].Update(crud_service_pb2.Record(key=key, value=value))
                except grpc.RpcError as e:
                    print(f"[SYNC-ERROR] Node at {port} is down during Update sync: {e}")
                    neighbor['alive'] = False

    def __delete_sync(self, key):
        for port, neighbor in self.__neighbors.items():
            if neighbor['alive']:
                try:
                    neighbor['stub'].Delete(crud_service_pb2.Key(key=key))
                except grpc.RpcError as e:
                    print(f"[SYNC-ERROR] Node at {port} is down during Delete sync: {e}")
                    neighbor['alive'] = False

    def __show(self):
        datas = [(k, v) for k, v in CLOUD_DB.items()]
        print(tabulate(datas, headers=["key", "value"], tablefmt="grid"))

    # --- Thread gửi heartbeat định kỳ đến các node láng giềng ---
    def __heartbeat_loop(self):
        while True:
            for port, neighbor in self.__neighbors.items():
                try:
                    response = neighbor['stub'].Heartbeat(crud_service_pb2.Empty(), timeout=2)
                    if response.status_code == 200:
                        if not neighbor['alive']:
                            print(f"[HEARTBEAT] Node at {port} has recovered!")
                        neighbor['alive'] = True
                except grpc.RpcError as e:
                    if neighbor['alive']:
                        print(f"[HEARTBEAT] Node at {port} is down: {e}")
                    neighbor['alive'] = False
            time.sleep(5)

    # --- Phương thức khôi phục dữ liệu ---
    def __recover_data(self):
        # Nếu CLOUD_DB rỗng, thử recovery từ một node khác theo chu kỳ
        while not CLOUD_DB:
            for port, neighbor in self.__neighbors.items():
                if neighbor['alive']:
                    try:
                        snapshot = neighbor['stub'].Snapshot(crud_service_pb2.Empty(), timeout=5)
                        if snapshot.records:  # Nếu có dữ liệu trong snapshot
                            for record in snapshot.records:
                                CLOUD_DB[record.key] = record.value
                            print(f"[RECOVERY] Data recovered from node {port}")
                            self.__show()
                            return  # Recovery thành công, thoát khỏi hàm
                    except grpc.RpcError as e:
                        print(f"[RECOVERY] Failed to get snapshot from node {port}: {e}")
            # Chờ thêm 5 giây rồi thử lại
            time.sleep(5)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crud_service_pb2_grpc.add_CloudStorageServicer_to_server(
        CloudStorage(), server=server
    )
    server.add_insecure_port(f"[::]:{server_port}")
    server.start()
    print(f"Serving on port: {server_port}")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
