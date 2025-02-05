import logging


import grpc
import crud_service_pb2
import crud_service_pb2_grpc


class Service:
    def __init__(self, channel):
        self.__stub = crud_service_pb2_grpc.CloudStorageStub(
            channel=grpc.insecure_channel(channel)
        )

    def menu(self):
        print(
            """
              1. Add new key-value pair\n
              2. Read a key\n
              """
        )
        choice = int(input("Your choice: "))
        match choice:
            case 1:
                print(self.__add())
            case 2:
                print(self.__read())
            case _:
                print("Invalid choice")

    def __add(self):
        key = input("Enter key: ")
        value = input("Enter value: ")
        return self.__stub.Create(crud_service_pb2.Record(key=key, value=value))

    def __read(self):
        key = input("Enter key: ")
        return self.__stub.Read(crud_service_pb2.Key(key=key))


# def run():
#     port = int(input("Server's port: "))
#     with grpc.insecure_channel(f"localhost:{port}") as channel:
#         stub = crud_service_pb2_grpc.CloudStorageStub(channel=channel)
#         while True:
#             key = input("Enter key: ")
#             value = input("Enter value: ")
#             record = crud_service_pb2.Record(key=key, value=value)
#             response = stub.Create(record)
#             print(response)
#             if input("Continue? ") != "y":
#                 break

if __name__ == "__main__":
    logging.basicConfig()
    port = input("Port: ")
    service = Service(f"localhost:{port}")
    while True:
        service.menu()
