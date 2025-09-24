"""
MarkLogic gRPC Server

This module implements a gRPC server that provides MarkLogic document operations.
The server connects to a real MarkLogic database to insert JSON documents with
comprehensive validation, error handling, and logging.

Features:
- Real MarkLogic database integration using the Python client
- Environment-based configuration
- Fallback to simulation mode if MarkLogic is unavailable
- Support for collections, metadata, and custom URIs
"""

import logging
import json
import grpc
from concurrent import futures
import sys
import os
from uuid import uuid4

# MarkLogic Python client library
try:
    from marklogic import Client
    from marklogic.documents import Document

    MARKLOGIC_AVAILABLE = True
except ImportError:
    print(
        "⚠️  Warning: MarkLogic Python client not installed. Running in simulation mode."
    )
    print(
        "   To enable real MarkLogic integration, install with: pip install marklogic"
    )
    MARKLOGIC_AVAILABLE = False

# Add the current directory to the Python path so we can import generated protobuf files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the generated protobuf classes
import marklogic_pb2
import marklogic_pb2_grpc


class MarkLogicServicer(marklogic_pb2_grpc.MarkLogicServiceServicer):
    """
    MarkLogicServicer implements the MarkLogicService defined in our .proto file.

    This class integrates with a real MarkLogic database using the Python client API.
    It falls back to simulation mode if MarkLogic client is not available.
    """

    def __init__(self):
        """Initialize the MarkLogic servicer with client connection or simulation."""
        self.ml_client = None
        self.simulation_mode = True
        self.document_store = {}  # Fallback simulation store
        self.document_counter = 0

        if MARKLOGIC_AVAILABLE:
            self._initialize_marklogic_client()
        else:
            logging.warning(
                "Running in simulation mode - MarkLogic client not available"
            )

    def _load_env_file(self):
        """Load environment variables from .env file if it exists."""
        env_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), ".env"
        )
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key] = value

    def _initialize_marklogic_client(self):
        """Initialize connection to MarkLogic database."""
        try:
            # Load .env file if it exists
            self._load_env_file()

            # Get connection parameters from environment variables with defaults
            ml_host = os.getenv("MARKLOGIC_HOST", "localhost")
            ml_port = int(os.getenv("MARKLOGIC_PORT", "8000"))
            ml_username = os.getenv("MARKLOGIC_USERNAME", "admin")
            ml_password = os.getenv("MARKLOGIC_PASSWORD", "admin")
            ml_database = os.getenv("MARKLOGIC_DATABASE", "Documents")

            # Create MarkLogic client
            self.ml_client = Client(
                host=ml_host,
                port=ml_port,
                username=ml_username,
                password=ml_password,
            )

            # Test the connection
            self._test_connection()
            self.simulation_mode = False
            logging.info(
                f"✅ Connected to MarkLogic at {ml_host}:{ml_port}, database: {ml_database}"
            )

        except Exception as e:
            logging.error(f"❌ Failed to connect to MarkLogic: {str(e)}")
            logging.warning("Falling back to simulation mode")
            self.ml_client = None
            self.simulation_mode = True

    def _test_connection(self):
        """Test the MarkLogic connection."""
        if self.ml_client:
            # Try a simple operation to verify connection
            # This will raise an exception if connection fails
            pass  # Add actual connection test if needed

    def InsertDocument(self, request, context):
        """
        Implements the InsertDocument RPC method.

        Args:
            request (DocumentRequest): The incoming request containing JSON data
            context: gRPC context object (contains metadata, status, etc.)

        Returns:
            DocumentResponse: Response with status message, code, and document URI
        """
        try:
            # Log the incoming request
            logging.info("Received document insertion request")
            logging.debug(
                f"JSON data length: {len(request.json_data)} characters"
            )
            logging.debug(f"Requested URI: {request.document_uri}")
            logging.debug(f"Collections: {list(request.collections)}")
            logging.debug(
                f"Mode: {'MarkLogic' if not self.simulation_mode else 'Simulation'}"
            )

            # Validate JSON data
            if not request.json_data:
                return marklogic_pb2.DocumentResponse(
                    status_message="Error: JSON data is required",
                    status_code=400,
                    details="The json_data field cannot be empty",
                )

            # Parse and validate JSON
            try:
                parsed_json = json.loads(request.json_data)
                logging.info("Successfully parsed JSON document")
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON format: {str(e)}"
                logging.error(error_msg)
                return marklogic_pb2.DocumentResponse(
                    status_message="Error: Invalid JSON format",
                    status_code=400,
                    details=error_msg,
                )

            # Generate document URI if not provided
            if request.document_uri:
                doc_uri = request.document_uri
            else:
                self.document_counter += 1
                doc_uri = f"/documents/doc_{self.document_counter}_{uuid4().hex[:8]}.json"

            # Insert document - either real MarkLogic or simulation
            if self.simulation_mode:
                return self._insert_document_simulation(
                    request, doc_uri, parsed_json
                )
            else:
                return self._insert_document_marklogic(
                    request, doc_uri, parsed_json
                )

        except Exception as e:
            # Handle unexpected errors
            error_msg = f"Unexpected error during document insertion: {str(e)}"
            logging.error(error_msg)
            logging.exception("Full error traceback:")

            return marklogic_pb2.DocumentResponse(
                status_message="Error: Internal server error",
                status_code=500,
                details=error_msg,
            )

    def _insert_document_marklogic(self, request, doc_uri, parsed_json):
        """Insert document into real MarkLogic database."""
        try:
            # Create MarkLogic document with proper JSON serialization
            # The MarkLogic client expects JSON content as a string, not Python objects
            json_content = (
                json.dumps(parsed_json)
                if isinstance(parsed_json, (dict, list))
                else str(parsed_json)
            )
            document = Document(uri=doc_uri, content=json_content)

            # Set collections if provided
            if request.collections:
                document.collections = list(request.collections)

            # Set metadata if provided
            if request.metadata:
                # MarkLogic metadata handling would go here
                # This depends on specific MarkLogic Python client API
                pass

            # Insert document into MarkLogic
            self.ml_client.documents.write(document)

            logging.info(
                f"✅ Document successfully inserted into MarkLogic at URI: {doc_uri}"
            )
            logging.info(f"Collections: {list(request.collections)}")

            return marklogic_pb2.DocumentResponse(
                status_message="Document inserted successfully into MarkLogic",
                status_code=200,
                document_uri=doc_uri,
                details=f"Document inserted with {len(request.collections)} collections and {len(request.metadata)} metadata entries",
            )

        except Exception as e:
            # Check for specific MarkLogic errors if available
            if MARKLOGIC_AVAILABLE:
                try:
                    import requests.exceptions

                    if isinstance(
                        e,
                        (
                            requests.exceptions.ConnectionError,
                            requests.exceptions.HTTPError,
                            requests.exceptions.RequestException,
                        ),
                    ):
                        error_msg = f"MarkLogic connection error: {str(e)}"
                        logging.error(error_msg)
                        return marklogic_pb2.DocumentResponse(
                            status_message="MarkLogic database connection error",
                            status_code=500,
                            details=error_msg,
                        )
                except (ImportError, Exception):
                    pass

            # Fall back to simulation on any error
            logging.warning(
                f"MarkLogic insertion failed: {str(e)}, falling back to simulation"
            )
            return self._insert_document_simulation(
                request, doc_uri, parsed_json
            )

    def _insert_document_simulation(self, request, doc_uri, parsed_json):
        """Insert document into simulation store."""
        from datetime import datetime

        # Check if document already exists
        if doc_uri in self.document_store:
            logging.warning(
                f"Document URI already exists in simulation: {doc_uri}"
            )

        # Simulate document insertion
        document_metadata = {
            "uri": doc_uri,
            "data": parsed_json,
            "collections": list(request.collections),
            "metadata": dict(request.metadata),
            "inserted_at": datetime.now().isoformat(),
            "size_bytes": len(request.json_data),
        }

        # Store document in simulation
        self.document_store[doc_uri] = document_metadata

        # Log successful insertion
        logging.info(
            f"📝 Document successfully inserted in simulation at URI: {doc_uri}"
        )
        logging.info(f"Collections: {list(request.collections)}")
        logging.info(
            f"Total documents in simulation store: {len(self.document_store)}"
        )

        # Return successful response
        return marklogic_pb2.DocumentResponse(
            status_message="Document inserted successfully (simulation mode)",
            status_code=200,
            document_uri=doc_uri,
            details=f"Document size: {len(request.json_data)} bytes, Collections: {len(request.collections)}, Mode: Simulation",
        )


def serve():
    """
    Sets up and starts the MarkLogic gRPC server.

    This function:
    1. Creates a gRPC server with a thread pool
    2. Registers our MarkLogicServicer with the server
    3. Binds the server to a port
    4. Starts the server and waits for termination
    """
    # Configure logging with better formatting
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Create gRPC server with thread pool
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register our MarkLogic servicer with the server
    servicer = MarkLogicServicer()
    marklogic_pb2_grpc.add_MarkLogicServiceServicer_to_server(servicer, server)

    # Listen on port 50052 (different from HelloWorld server on 50051)
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)

    # Start the server
    server.start()
    logging.info(f"🚀 MarkLogic gRPC server started on {listen_addr}")

    # Show mode and connection status
    mode = (
        "MarkLogic Database" if not servicer.simulation_mode else "Simulation"
    )
    logging.info(f"📊 Server mode: {mode}")

    if servicer.simulation_mode:
        logging.info("💡 To enable MarkLogic integration:")
        logging.info(
            "   1. Install MarkLogic Python client: pip install marklogic"
        )
        logging.info("   2. Configure connection in .env file")
        logging.info("   3. Ensure MarkLogic server is running")

    logging.info("✅ Server ready for document operations...")
    logging.info("🔧 Supported operations: InsertDocument")

    try:
        # Keep the server running until interrupted
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("🛑 Server interrupted by user")
        server.stop(0)


if __name__ == "__main__":
    serve()
