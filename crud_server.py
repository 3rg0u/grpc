import grpc
import crud_service_pb2
import crud_service_pb2_grpc

from concurrent import futures
import logging

from nodes import NODES
from tabulate import tabulate

CLOUD_DB = {}


server_port = input("Choose a port to serve: ")


class CloudStorage(crud_service_pb2_grpc.CloudStorageServicer):
    def __init__(self):
        self.__neibor_stubs = [
            crud_service_pb2_grpc.CloudStorageStub(
                channel=grpc.insecure_channel(f"localhost:{port}")
            )
            for port in NODES
            if port != server_port
        ]

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

    def __add_sync(self, key, value):
        for stub in self.__neibor_stubs:
            stub.Create(crud_service_pb2.Record(key=key, value=value))

    def __update_sync(self, key, value):
        for stub in self.__neibor_stubs:
            stub.Update(crud_service_pb2.Record(key=key, value=value))

    def __delete_sync(self, key):
        for stub in self.__neibor_stubs:
            stub.Delete(crud_service_pb2.Key(key=key))

    def __show(self):
        datas = [(k, v) for k, v in CLOUD_DB.items()]
        print(tabulate(datas, headers=["key", "value"], tablefmt="grid"))


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
