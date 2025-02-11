import grpc
import grpc._channel


from crud_services import crud_service_pb2, crud_service_pb2_grpc, nodes


class Service:
    def __init__(self):
        addresses = nodes.NODES

        self.__stubs = []
        for address in addresses:
            channel = grpc.insecure_channel(f"localhost:{address}")
            stub = crud_service_pb2_grpc.CloudStorageStub(channel)
            self.__stubs.append((address, stub))

        print("Using nodes:")
        for address, _ in self.__stubs:
            print(" -", address)

    def __call_rpc(self, rpc_method, request):
        for address, stub in self.__stubs:
            try:
                return getattr(stub, rpc_method)(request, timeout=5)
            except grpc.RpcError as e:
                print(f"Node {address} failed!")
        print("All nodes are unreachable!")
        return None

    def create(self, key, value):
        return self.__call_rpc("Create", crud_service_pb2.Record(key=key, value=value))

    def read(self, key):
        return self.__call_rpc("Read", crud_service_pb2.Key(key=key))

    def update(self, key, value):
        return self.__call_rpc("Update", crud_service_pb2.Record(key=key, value=value))

    def delete(self, key):
        return self.__call_rpc("Delete", crud_service_pb2.Key(key=key))
