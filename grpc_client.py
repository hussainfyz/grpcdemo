import grpc
import data_processor_pb2
import data_processor_pb2_grpc

# Connect to gRPC server
channel = grpc.insecure_channel("localhost:50051")
stub = data_processor_pb2_grpc.DataProcessorStub(channel)

# Create test data
test_data = [data_processor_pb2.DataItem(id=i, value=i*10) for i in range(5)]
request = data_processor_pb2.ProcessRequest(data=test_data)

# Call gRPC method
response = stub.ProcessData(request)
print(f"Processed Records: {response.processed_records}")
