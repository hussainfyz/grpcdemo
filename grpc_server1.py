import grpc
from concurrent import futures
import time,os
print(os.listdir(os.getcwd()))
import data_service_pb2
import data_service_pb2_grpc
from prometheus_client import start_http_server, Counter, Histogram

# Define Prometheus Metrics
REQUEST_COUNT = Counter("grpc_requests_total", "Total number of gRPC requests", ["method"])
REQUEST_LATENCY = Histogram("grpc_request_duration_seconds", "gRPC request latency", ["method"])

class DataServiceServicer(data_service_pb2_grpc.DataServiceServicer):
    def GetLargeData(self, request, context):
        """Streams large dataset to the client"""
        REQUEST_COUNT.labels(method="GetLargeData").inc()  # Increment request counter
        start_time = time.time()
        
        for i in range(request.num_records):
            record = data_service_pb2.DataRecord(
                id=i, name=f"Item {i}", value=i * 1.5, category="A"
            )
            yield record  # Streaming response
        
        REQUEST_LATENCY.labels(method="GetLargeData").observe(time.time() - start_time)  # Record latency

def serve():
    # Start Prometheus HTTP metrics server on port 8000
    start_http_server(8000)

    # Start gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_service_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    
    print("🚀 gRPC Server is running on port 50051")
    print("📊 Prometheus metrics available at http://localhost:8000/metrics")
    
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
