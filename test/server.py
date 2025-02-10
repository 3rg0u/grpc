import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def Greeting(self, request, context):
        return f"Hello, {request.name}"
