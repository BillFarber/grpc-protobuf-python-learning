"""
gRPC HelloWorld Client

This module implements a simple gRPC client that connects to the HelloService
and sends greeting requests to the server.
"""

import logging
import grpc
import sys
import os

# Add the current directory to the Python path so we can import generated protobuf files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# These imports will work after we generate the protobuf Python files
import hello_pb2
import hello_pb2_grpc


def run_client(name="World"):
    """
    Creates a gRPC client and sends a HelloRequest to the server.

    Args:
        name (str): The name to include in the greeting request

    Returns:
        str: The greeting response from the server, or None if there was an error
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Define the server address
    # This should match the address where the server is listening
    server_address = "localhost:50051"

    # Create a gRPC channel
    # A channel represents a connection to a gRPC server
    # insecure_channel creates a channel without SSL/TLS encryption
    # (for production, you'd typically use secure_channel with SSL/TLS)
    with grpc.insecure_channel(server_address) as channel:
        try:
            # Create a stub (client)
            # The stub provides the methods to call the remote service
            # It's generated from our .proto file and contains all the RPC methods
            stub = hello_pb2_grpc.HelloServiceStub(channel)

            # Create a HelloRequest message
            # This is the message we'll send to the server
            request = hello_pb2.HelloRequest(name=name)

            logging.info(f"Sending request with name: {request.name}")

            # Call the SayHello method on the server
            # This is a synchronous call - it will block until the server responds
            # The method name matches what we defined in our .proto file
            response = stub.SayHello(request)

            logging.info(f"Received response: {response.message}")

            # Return the message from the response
            return response.message

        except grpc.RpcError as e:
            # Handle gRPC-specific errors
            logging.error(f"gRPC error occurred: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            # Handle any other errors
            logging.error(f"Unexpected error: {str(e)}")
            return None


def main():
    """
    Main function that demonstrates different ways to use the client.
    """
    print("gRPC HelloWorld Client")
    print("=" * 50)

    # Example 1: Default greeting
    print("\nExample 1: Default greeting")
    response = run_client()
    if response:
        print(f"Server responded: {response}")

    # Example 2: Custom name
    print("\nExample 2: Custom name")
    response = run_client("Alice")
    if response:
        print(f"Server responded: {response}")

    # Example 3: Another custom name
    print("\nExample 3: Another custom name")
    response = run_client("Bob")
    if response:
        print(f"Server responded: {response}")

    # Example 4: Interactive mode
    print("\nExample 4: Interactive mode")
    try:
        while True:
            user_name = input(
                "\nEnter a name to greet (or 'quit' to exit): "
            ).strip()
            if user_name.lower() in ["quit", "exit", "q"]:
                break
            if user_name:
                response = run_client(user_name)
                if response:
                    print(f"Server responded: {response}")
            else:
                print("Please enter a valid name.")
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
