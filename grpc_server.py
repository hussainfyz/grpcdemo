import grpc
from concurrent import futures
import data_processor_pb2
import data_processor_pb2_grpc

class DataProcessorServicer(data_processor_pb2_grpc.DataProcessorServicer):
    def ProcessData(self, request, context):
        """Processes data items and returns count"""
        processed_data = [{"id": item.id, "processed_value": item.value * 2} for item in request.data]
        return data_processor_pb2.ProcessResponse(processed_records=len(processed_data))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_processor_pb2_grpc.add_DataProcessorServicer_to_server(DataProcessorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
