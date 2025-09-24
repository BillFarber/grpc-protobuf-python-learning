"""
MarkLogic gRPC Client

This module implements a gRPC client that connects to the MarkLogic service
and demonstrates document insertion operations.
"""

import logging
import json
import grpc
import sys
import os

# Add the current directory to the Python path so we can import generated protobuf files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the generated protobuf classes
import marklogic_pb2
import marklogic_pb2_grpc


def insert_document(
    json_data,
    document_uri=None,
    collections=None,
    metadata=None,
    server_address="localhost:50052",
):
    """
    Inserts a document into MarkLogic via gRPC.

    Args:
        json_data (str or dict): The JSON data to insert (string or dict)
        document_uri (str, optional): URI for the document in MarkLogic
        collections (list, optional): List of collection names
        metadata (dict, optional): Document metadata as key-value pairs
        server_address (str): Address of the MarkLogic gRPC server

    Returns:
        DocumentResponse: The response from the server
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Convert dict/list to JSON string if necessary
    # Handle both dict objects and list/array objects
    if isinstance(json_data, (dict, list)):
        json_str = json.dumps(json_data, indent=2)
    else:
        # If it's already a string, use as-is (for pre-formatted JSON)
        json_str = str(json_data)

    # Set default values
    if collections is None:
        collections = []
    if metadata is None:
        metadata = {}

    # Create gRPC channel and stub
    with grpc.insecure_channel(server_address) as channel:
        try:
            # Create the service stub
            stub = marklogic_pb2_grpc.MarkLogicServiceStub(channel)

            # Create the request
            request = marklogic_pb2.DocumentRequest(
                json_data=json_str,
                document_uri=document_uri or "",
                collections=collections,
                metadata=metadata,
            )

            logging.info("Sending document insertion request...")
            logging.debug(
                f"JSON data: {json_str[:100]}{'...' if len(json_str) > 100 else ''}"
            )
            logging.debug(f"Document URI: {document_uri}")
            logging.debug(f"Collections: {collections}")

            # Call the InsertDocument method
            response = stub.InsertDocument(request)

            # Log the response
            if response.status_code == 200:
                logging.info(f"✅ Success: {response.status_message}")
                logging.info(f"Document URI: {response.document_uri}")
            else:
                logging.error(
                    f"❌ Error {response.status_code}: {response.status_message}"
                )

            if response.details:
                logging.info(f"Details: {response.details}")

            return response

        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return None


def run_examples():
    """
    Demonstrates various document insertion scenarios.
    """
    print("MarkLogic gRPC Client - Document Insertion Examples")
    print("=" * 60)

    # Example 1: Simple JSON object
    print("\n📄 Example 1: Simple JSON document")
    simple_doc = {
        "title": "Sample Document",
        "author": "John Doe",
        "created": "2024-01-01",
        "content": "This is a sample document for MarkLogic.",
    }

    response = insert_document(
        json_data=simple_doc, collections=["examples", "samples"]
    )

    # Example 2: Complex nested JSON
    print("\n📄 Example 2: Complex nested JSON")
    complex_doc = {
        "customer": {
            "id": 12345,
            "name": "Acme Corporation",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip": "12345",
            },
            "contacts": [
                {"type": "email", "value": "contact@acme.com"},
                {"type": "phone", "value": "+1-555-0123"},
            ],
        },
        "orders": [
            {"id": 1001, "total": 299.99, "status": "shipped"},
            {"id": 1002, "total": 149.50, "status": "pending"},
        ],
        "metadata": {"created_by": "data_import_service", "version": "1.0"},
    }

    response = insert_document(
        json_data=complex_doc,
        document_uri="/customers/12345.json",
        collections=["customers", "active"],
        metadata={"source": "crm_system", "priority": "high"},
    )

    # Example 3: Array document
    print("\n📄 Example 3: JSON array document")
    array_doc = [
        {"name": "Alice", "age": 30, "department": "Engineering"},
        {"name": "Bob", "age": 25, "department": "Marketing"},
        {"name": "Charlie", "age": 35, "department": "Sales"},
    ]

    response = insert_document(
        json_data=array_doc,
        collections=["employees", "directory"],
        metadata={"type": "employee_list"},
    )

    # Example 4: Error case - invalid JSON
    print("\n📄 Example 4: Invalid JSON (error case)")
    invalid_json = '{"name": "Test", "invalid": }'

    response = insert_document(json_data=invalid_json)

    print("\n🎉 Examples completed!")


def interactive_mode():
    """
    Interactive mode for testing document insertion.
    """
    print("\n🔧 Interactive Mode")
    print("Enter JSON documents to insert (type 'quit' to exit)")

    while True:
        try:
            print("\nOptions:")
            print("1. Enter JSON manually")
            print("2. Use predefined example")
            print("3. Quit")

            choice = input("Select option (1-3): ").strip()

            if choice == "3" or choice.lower() == "quit":
                break
            elif choice == "1":
                print("\nEnter JSON data (press Enter twice to submit):")
                json_lines = []
                while True:
                    line = input()
                    if line == "" and json_lines:
                        break
                    json_lines.append(line)

                json_data = "\n".join(json_lines)

                # Optional parameters
                uri = input("Document URI (optional): ").strip() or None
                collections_input = input(
                    "Collections (comma-separated, optional): "
                ).strip()
                collections = (
                    [c.strip() for c in collections_input.split(",")]
                    if collections_input
                    else []
                )

                response = insert_document(
                    json_data=json_data,
                    document_uri=uri,
                    collections=collections,
                )

            elif choice == "2":
                example_doc = {
                    "test": True,
                    "timestamp": "2024-01-01T12:00:00Z",
                    "message": "This is a test document from interactive mode",
                }

                response = insert_document(
                    json_data=example_doc, collections=["interactive", "test"]
                )

            else:
                print("Invalid choice. Please select 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def main():
    """
    Main function that runs the client examples and interactive mode.
    """
    try:
        # Run predefined examples
        run_examples()

        # Ask if user wants interactive mode
        while True:
            choice = (
                input("\nWould you like to try interactive mode? (y/n): ")
                .strip()
                .lower()
            )
            if choice in ["y", "yes"]:
                interactive_mode()
                break
            elif choice in ["n", "no"]:
                print("Thanks for using the MarkLogic gRPC client!")
                break
            else:
                print("Please enter 'y' or 'n'")

    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
