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
        while True:
            print(
                """
                1. Add a new record\n
                2. Read a key\n
                3. Update an existing record\n
                4. Delete a record
                """
            )
            try:
                choice = int(input("Your choice: "))
            except ValueError:
                print("Invalid choice!")
                continue
            match choice:
                case 1:
                    print(self.__add())
                case 2:
                    print(self.__read())
                case 3:
                    print(self.__update())
                case 4:
                    print(self.__delete())
                case _:
                    print("Invalid choice")

    def __add(self):
        key = input("Enter key: ")
        value = input("Enter value: ")
        return self.__stub.Create(crud_service_pb2.Record(key=key, value=value))

    def __read(self):
        key = input("Enter key: ")
        return self.__stub.Read(crud_service_pb2.Key(key=key))

    def __update(self):
        key = input("Enter key: ")
        value = input("Enter value: ")
        return self.__stub.Update(crud_service_pb2.Record(key=key, value=value))

    def __delete(self):
        key = input("Enter key: ")
        return self.__stub.Delete(crud_service_pb2.Key(key=key))


if __name__ == "__main__":
    logging.basicConfig()
    port = input("Port: ")
    service = Service(f"localhost:{port}")
    service.menu()
