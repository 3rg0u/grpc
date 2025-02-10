import grpc
import crud_service_pb2
import crud_service_pb2_grpc

class Service:
    def __init__(self):
        """
        Sử dụng danh sách các node cố định: 6677, 7766, 6767.
        Nếu địa chỉ chỉ là số cổng, tự thêm "localhost:" vào.
        """
        # Danh sách địa chỉ cố định
        addresses = ["6677", "7766", "6767"]
        
        self.__stubs = []
        for address in addresses:
            if ':' not in address:
                address = "localhost:" + address
            channel = grpc.insecure_channel(address)
            stub = crud_service_pb2_grpc.CloudStorageStub(channel)
            self.__stubs.append((address, stub))

        print("Using nodes:")
        for address, _ in self.__stubs:
            print(" -", address)

    def __call_rpc(self, rpc_method, request):
        """
        Duyệt qua danh sách các node cố định để gọi RPC.
        Nếu một node không phản hồi (bị tắt) sẽ bỏ qua và chuyển sang node khác.
        """
        for address, stub in self.__stubs:
            try:
                # Thêm timeout để không bị treo nếu node không phản hồi
                return getattr(stub, rpc_method)(request, timeout=5)
            except grpc.RpcError as e:
                print(f"Node {address} failed: {e}")
        print("All nodes are unreachable!")
        return None

    def __add(self):
        key = input("Enter key: ")
        value = input("Enter value: ")
        return self.__call_rpc("Create", crud_service_pb2.Record(key=key, value=value))

    def __read(self):
        key = input("Enter key: ")
        return self.__call_rpc("Read", crud_service_pb2.Key(key=key))

    def __update(self):
        key = input("Enter key: ")
        value = input("Enter value: ")
        return self.__call_rpc("Update", crud_service_pb2.Record(key=key, value=value))

    def __delete(self):
        key = input("Enter key: ")
        return self.__call_rpc("Delete", crud_service_pb2.Key(key=key))

    def menu(self):
        while True:
            print(
                """
                1. Add a new record
                2. Read a key
                3. Update an existing record
                4. Delete a record
                """
            )
            try:
                choice = int(input("Your choice: "))
            except ValueError:
                print("Invalid choice!")
                continue

            if choice == 1:
                response = self.__add()
                if response:
                    print(response)
            elif choice == 2:
                response = self.__read()
                if response:
                    print(response)
            elif choice == 3:
                response = self.__update()
                if response:
                    print(response)
            elif choice == 4:
                response = self.__delete()
                if response:
                    print(response)
            else:
                print("Invalid choice")

if __name__ == "__main__":
    import logging
    logging.basicConfig()
    service = Service()
    service.menu()
