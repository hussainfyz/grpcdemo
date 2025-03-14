import grpc
import data_service_pb2
import data_service_pb2_grpc

# Connect to gRPC server
GRPC_SERVER="route-improved-orangutan-fayaz-912-dev.apps.rm2.thpm.p1.openshiftapps.com:50051"
channel = grpc.insecure_channel(GRPC_SERVER)
stub = data_service_pb2_grpc.DataServiceStub(channel)

# Send a request for 5 records
request = data_service_pb2.DataRequest(num_records=5)

# Call gRPC method and stream response
print("📥 Receiving records from gRPC server:")
for response in stub.GetLargeData(request):
    print(f"📌 ID: {response.id}, Name: {response.name}, Value: {response.value}, Category: {response.category}")
