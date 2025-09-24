"""
gRPC HelloWorld Server

This module implements a simple gRPC server that provides a HelloService.
The server listens for incoming requests and responds with personalized greetings.
"""

import logging
import grpc
from concurrent import futures
import sys
import os

# Add the current directory to the Python path so we can import generated protobuf files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# These imports will work after we generate the protobuf Python files
# hello_pb2 contains the message classes (HelloRequest, HelloResponse)
# hello_pb2_grpc contains the service classes and stubs
import hello_pb2
import hello_pb2_grpc


class HelloServicer(hello_pb2_grpc.HelloServiceServicer):
    """
    HelloServicer implements the HelloService defined in our .proto file.

    This class inherits from the generated HelloServiceServicer class,
    which provides the interface we need to implement our service methods.
    """

    def SayHello(self, request, context):
        """
        Implements the SayHello RPC method.

        Args:
            request (HelloRequest): The incoming request containing the name to greet
            context: gRPC context object (contains metadata, status, etc.)

        Returns:
            HelloResponse: A response containing the personalized greeting
        """
        # Log the incoming request for debugging
        logging.info(f"Received request for name: {request.name}")

        # Create the response message
        # We're accessing the 'name' field from the HelloRequest message
        greeting_message = (
            f"Hello, {request.name}! Welcome to gRPC with Protocol Buffers!"
        )

        # Create and return a HelloResponse message
        # The HelloResponse constructor accepts keyword arguments that match
        # the field names defined in our .proto file
        response = hello_pb2.HelloResponse(message=greeting_message)

        logging.info(f"Sending response: {response.message}")
        return response


def serve():
    """
    Sets up and starts the gRPC server.

    This function:
    1. Creates a gRPC server with a thread pool
    2. Registers our HelloServicer with the server
    3. Binds the server to a port
    4. Starts the server and waits for termination
    """
    # Configure logging to see what's happening
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Create a gRPC server
    # ThreadPoolExecutor allows the server to handle multiple requests concurrently
    # max_workers=10 means we can handle up to 10 concurrent requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register our HelloServicer with the server
    # This tells gRPC that our HelloServicer class should handle
    # requests for the HelloService
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloServicer(), server)

    # Define the address and port where the server will listen
    listen_addr = "[::]:50051"  # Listen on all interfaces, port 50051
    server.add_insecure_port(listen_addr)

    # Start the server
    server.start()
    logging.info(f"gRPC server started on {listen_addr}")
    logging.info("Server is ready to receive requests...")

    try:
        # Keep the server running
        # server.wait_for_termination() blocks until the server is stopped
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Server interrupted by user")
        server.stop(0)


if __name__ == "__main__":
    serve()
