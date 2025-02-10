# test_heartbeat.py
import grpc
import time

import crud_service_pb2
import crud_service_pb2_grpc

def test_heartbeat(server_address):
    channel = grpc.insecure_channel(server_address)
    stub = crud_service_pb2_grpc.CloudStorageStub(channel)
    try:
        response = stub.Heartbeat(crud_service_pb2.Empty(), timeout=2)
        print(f"Heartbeat to {server_address}: {response.status_code} - {response.message}")
    except grpc.RpcError as e:
        print(f"Error calling heartbeat on {server_address}: {e}")

if __name__ == "__main__":
    addresses = ["localhost:50051", "localhost:50052", "localhost:50053"]
    while True:
        for addr in addresses:
            test_heartbeat(addr)
        time.sleep(5)
