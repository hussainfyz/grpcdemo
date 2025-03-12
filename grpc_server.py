import grpc
from concurrent import futures
import time
import data_processor_pb2
import data_processor_pb2_grpc
from prometheus_client import start_http_server, Counter, Histogram

# Define Prometheus Metrics
REQUEST_COUNT = Counter("grpc_requests_total", "Total number of gRPC requests", ["method"])
REQUEST_LATENCY = Histogram("grpc_request_duration_seconds", "gRPC request latency", ["method"])

class DataProcessorServicer(data_processor_pb2_grpc.DataProcessorServicer):
    def ProcessData(self, request, context):
        """Processes data items and returns count"""
        REQUEST_COUNT.labels(method="ProcessData").inc()  # Increment request counter
        
        start_time = time.time()
        processed_data = [{"id": item.id, "processed_value": item.value * 2} for item in request.data]
        response = data_processor_pb2.ProcessResponse(processed_records=len(processed_data))
        
        REQUEST_LATENCY.labels(method="ProcessData").observe(time.time() - start_time)  # Record latency
        return response

def serve():
    # Start Prometheus HTTP metrics server on port 8000
    start_http_server(8000)

    # Start gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_processor_pb2_grpc.add_DataProcessorServicer_to_server(DataProcessorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    
    print("🚀 gRPC Server is running on port 50051")
    print("📊 Prometheus metrics available at http://localhost:8000/metrics")
    
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
