import grpc
import crud_service_pb2
import crud_service_pb2_grpc

from concurrent import futures
import logging
import threading
import time

from nodes import NODES
from tabulate import tabulate

CLOUD_DB = {}

server_port = input("Choose a port to serve: ")

class CloudStorage(crud_service_pb2_grpc.CloudStorageServicer):
    def __init__(self):
        # Khởi tạo các neighbor node (ngoại trừ chính node đang chạy)
        self.__neighbors = {}
        for port in NODES:
            if port != server_port:
                self.__neighbors[port] = {
                    'stub': crud_service_pb2_grpc.CloudStorageStub(
                        channel=grpc.insecure_channel(f"localhost:{port}")
                    ),
                    'alive': True
                }
        # Bắt đầu thread gửi heartbeat định kỳ
        heartbeat_thread = threading.Thread(target=self.__heartbeat_loop, daemon=True)
        heartbeat_thread.start()

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

    # --- Phương thức đồng bộ với các neighbor ---
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

    # --- Phương thức Heartbeat: được các neighbor gọi để kiểm tra tình trạng node ---
    def Heartbeat(self, request, context):
        return crud_service_pb2.Response(status_code=200, message="Alive")

    # --- Thread gửi heartbeat định kỳ đến các neighbor ---
    def __heartbeat_loop(self):
        while True:
            for port, neighbor in self.__neighbors.items():
                try:
                    # Gọi RPC Heartbeat (giả sử bạn đã định nghĩa message Empty trong proto)
                    response = neighbor['stub'].Heartbeat(crud_service_pb2.Empty())
                    if response.status_code == 200:
                        if not neighbor['alive']:
                            print(f"[HEARTBEAT] Node at {port} has recovered!")
                        neighbor['alive'] = True
                except grpc.RpcError as e:
                    if neighbor['alive']:
                        print(f"[HEARTBEAT] Node at {port} is down: {e}")
                    neighbor['alive'] = False
            time.sleep(5)  # Gửi heartbeat mỗi 5 giây

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
