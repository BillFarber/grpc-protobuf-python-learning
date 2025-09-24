# gRPC & Protocol Buffers Learning Project 🚀

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![gRPC](https://img.shields.io/badge/gRPC-1.60.0-green?style=flat-square&logo=grpc)](https://grpc.io/)
[![Protocol Buffers](https://img.shields.io/badge/Protobuf-4.25.1-orange?style=flat-square)](https://developers.google.com/protocol-buffers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

A comprehensive Python project demonstrating gRPC (Google Remote Procedure Call) and Protocol Buffers (Protobuf) concepts through practical examples including a HelloWorld service and a MarkLogic document insertion service.

> **Perfect for mid-level Python developers learning microservices communication patterns!**

## 🎯 Learning Objectives

This project will help you understand:
- What gRPC is and how it works
- How Protocol Buffers define service contracts
- How to implement gRPC servers and clients in Python
- The request-response flow in gRPC applications

## 📋 What is gRPC?

**gRPC** is a modern, high-performance RPC (Remote Procedure Call) framework that can run in any environment. Key features:

- **Language Agnostic**: Works across different programming languages
- **High Performance**: Uses HTTP/2 for transport and Protocol Buffers for serialization
- **Type Safety**: Strongly typed contracts using Protocol Buffers
- **Streaming**: Supports various streaming patterns (unary, server streaming, client streaming, bidirectional)

## 📋 What are Protocol Buffers?

**Protocol Buffers (Protobuf)** is Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. Benefits:

- **Efficient**: Smaller and faster than JSON or XML
- **Strongly Typed**: Enforces data structure contracts
- **Backward Compatible**: Can evolve schemas without breaking existing code
- **Code Generation**: Automatically generates client/server code

## 🏗️ Project Structure

```
grpc-hello-world/
│
├── proto/
│   ├── hello.proto          # HelloWorld Protocol Buffer definition
│   └── marklogic.proto      # MarkLogic Protocol Buffer definition
│
├── src/
│   ├── server.py            # HelloWorld gRPC server
│   ├── client.py            # HelloWorld gRPC client
│   ├── marklogic_server.py  # MarkLogic gRPC server
│   ├── marklogic_client.py  # MarkLogic gRPC client
│   ├── hello_pb2.py         # Generated: HelloWorld message classes
│   ├── hello_pb2_grpc.py    # Generated: HelloWorld service classes
│   ├── marklogic_pb2.py     # Generated: MarkLogic message classes
│   └── marklogic_pb2_grpc.py # Generated: MarkLogic service classes
│
├── requirements.txt         # Python dependencies
├── generate_proto.sh        # Script to generate Python code from .proto
├── run_example.sh          # Script to run HelloWorld example
├── marklogic_demo.sh       # Script to run MarkLogic example
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Generate Python Code from Protocol Buffers

```bash
# Make the script executable and run it
chmod +x generate_proto.sh
./generate_proto.sh
```

Or manually:
```bash
cd proto
python -m grpc_tools.protoc --python_out=../src --grpc_python_out=../src hello.proto
```

### 3. Run the Server

```bash
cd src
python server.py
```

You should see:
```
2024-XX-XX XX:XX:XX - INFO - gRPC server started on [::]:50051
2024-XX-XX XX:XX:XX - INFO - Server is ready to receive requests...
```

### 4. Run the Client (in a new terminal)

```bash
cd src
python client.py
```

## 📖 Understanding the Code

### Protocol Buffer Definition (`proto/hello.proto`)

```protobuf
syntax = "proto3";

package hello;

// Service definition
service HelloService {
    rpc SayHello (HelloRequest) returns (HelloResponse);
}

// Request message
message HelloRequest {
    string name = 1;
}

// Response message
message HelloResponse {
    string message = 1;
}
```

**Key Concepts:**
- **Service**: Defines the RPC methods available
- **Messages**: Define the structure of data exchanged
- **Field Numbers**: Unique identifiers for each field (never change these!)

### Server Implementation (`src/server.py`)

The server:
1. **Inherits from generated service class**: `HelloServiceServicer`
2. **Implements RPC methods**: `SayHello`
3. **Handles requests**: Receives `HelloRequest`, returns `HelloResponse`
4. **Runs on port 50051**: Listens for incoming connections

**Key Components:**
```python
class HelloServicer(hello_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        # Process request.name
        # Return HelloResponse
```

### Client Implementation (`src/client.py`)

The client:
1. **Creates a channel**: Connection to the server
2. **Creates a stub**: Interface to call remote methods
3. **Makes RPC calls**: Sends `HelloRequest`, receives `HelloResponse`

**Key Components:**
```python
with grpc.insecure_channel('localhost:50051') as channel:
    stub = hello_pb2_grpc.HelloServiceStub(channel)
    response = stub.SayHello(hello_pb2.HelloRequest(name="World"))
```

## 🔄 Request-Response Flow

1. **Client** creates a `HelloRequest` with a name
2. **Client** sends the request to the server via gRPC
3. **Server** receives the request and extracts the name
4. **Server** creates a `HelloResponse` with a personalized greeting
5. **Server** sends the response back to the client
6. **Client** receives and displays the response

## 🛠️ Generated Files

When you run the Protocol Buffer compiler, it generates:

- **`hello_pb2.py`**: Contains message classes (`HelloRequest`, `HelloResponse`)
- **`hello_pb2_grpc.py`**: Contains service classes (`HelloServiceServicer`, `HelloServiceStub`)

These files provide the Python interfaces for your defined Protocol Buffer messages and services.

## 🧪 Testing Different Scenarios

### Basic Usage
```bash
python client.py
```

### Custom Names
Edit `client.py` or use the interactive mode to test with different names.

### Error Handling
- Stop the server and run the client to see connection error handling
- Send empty names to test validation

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've generated the Protocol Buffer files first
   ```bash
   ./generate_proto.sh
   ```

2. **Connection Refused**: Ensure the server is running before starting the client

3. **Port Already in Use**: Change the port number in both server and client if 50051 is occupied

4. **Permission Denied**: Make scripts executable:
   ```bash
   chmod +x generate_proto.sh run_example.sh
   ```

### Debugging Tips

- Check server logs for incoming requests
- Use `logging.DEBUG` for more detailed output
- Verify that generated files exist in the `src/` directory

## �️ MarkLogic gRPC Service

This project also includes a MarkLogic document insertion service that demonstrates more complex gRPC operations:

### Features
- **Document Insertion**: Insert JSON documents via gRPC
- **Collection Management**: Assign documents to collections
- **Metadata Support**: Add custom metadata to documents
- **Error Handling**: Comprehensive error responses
- **Status Reporting**: Detailed operation status and codes

### Protocol Buffer Definition (`proto/marklogic.proto`)

```protobuf
service MarkLogicService {
    rpc InsertDocument (DocumentRequest) returns (DocumentResponse);
}

message DocumentRequest {
    string json_data = 1;          // JSON document as string
    string document_uri = 2;       // Optional URI
    repeated string collections = 3; // Collection names
    map<string, string> metadata = 4; // Custom metadata
}

message DocumentResponse {
    string status_message = 1;     // Human-readable status
    int32 status_code = 2;        // HTTP-like status code
    string document_uri = 3;      // Where document was stored
    string details = 4;           // Additional information
}
```

### Usage Examples

**Start the MarkLogic server:**
```bash
cd src
python marklogic_server.py  # Runs on port 50052
```

**Run the client examples:**
```bash
cd src
python marklogic_client.py
```

**Or use the demo script:**
```bash
./marklogic_demo.sh
```

### Sample Document Insertion

```python
from marklogic_client import insert_document

# Insert a complex JSON document
document = {
    "customer": {
        "name": "ACME Corp",
        "orders": [{"id": 1, "total": 99.99}]
    }
}

response = insert_document(
    json_data=document,
    document_uri="/customers/acme.json",
    collections=["customers", "enterprise"],
    metadata={"source": "api", "priority": "high"}
)

print(f"Status: {response.status_code}")
print(f"Message: {response.status_message}")
print(f"URI: {response.document_uri}")
```

## 🏢 MarkLogic Database Integration

The MarkLogic gRPC server can connect to a real MarkLogic database for document insertion. By default, it runs in **simulation mode** and will automatically attempt to connect to MarkLogic if the client library is available.

### Prerequisites for Real Integration

1. **MarkLogic Server**: Running MarkLogic instance (version 9.0+)
2. **MarkLogic Python Client**: Install the client library
3. **Database Configuration**: Proper connection settings

### Installation Steps

1. **Install MarkLogic Python Client**:
   ```bash
   pip install marklogic==1.4.0
   ```

2. **Run the Setup Script**:
   ```bash
   ./setup_marklogic.sh
   ```

3. **Configure Connection Settings**:
   Edit the `.env` file created by the setup script:
   ```env
   MARKLOGIC_HOST=localhost
   MARKLOGIC_PORT=8000
   MARKLOGIC_USERNAME=admin
   MARKLOGIC_PASSWORD=your_password
   MARKLOGIC_DATABASE=Documents
   ```

### Server Modes

The MarkLogic gRPC server operates in two modes:

#### 🔌 **MarkLogic Mode** (Real Integration)
- Connects to actual MarkLogic database
- Inserts documents into the specified database
- Uses MarkLogic collections and metadata
- Requires MarkLogic server to be running

#### 📝 **Simulation Mode** (Fallback)
- In-memory document storage for testing
- No MarkLogic server required
- Perfect for development and learning
- Automatic fallback if connection fails

### Connection Status

The server automatically detects the mode on startup:

```bash
# MarkLogic Mode
✅ Connected to MarkLogic at localhost:8000, database: Documents
📊 Server mode: MarkLogic Database

# Simulation Mode  
⚠️  Warning: MarkLogic Python client not installed. Running in simulation mode.
📊 Server mode: Simulation
💡 To enable MarkLogic integration:
   1. Install MarkLogic Python client: pip install marklogic
   2. Configure connection in .env file
   3. Ensure MarkLogic server is running
```

### Testing the Integration

1. **Start MarkLogic Server** (if using real integration)
2. **Run the MarkLogic gRPC server**:
   ```bash
   cd src
   python marklogic_server.py
   ```
3. **Test with client**:
   ```bash
   python marklogic_client.py
   ```

The client will work identically in both modes, making it easy to develop without a MarkLogic server and then deploy to production with real database integration.

### Error Handling

The server gracefully handles connection issues:
- **Connection failure**: Automatically falls back to simulation mode
- **Authentication errors**: Detailed logging and error responses  
- **Network issues**: Retry logic and fallback mechanisms

## 🚀 Next Steps

Once you understand these examples, consider exploring:

1. **Streaming RPCs**: Server streaming, client streaming, bidirectional streaming
2. **Error Handling**: Custom error codes and status messages
3. **Authentication**: Adding authentication and authorization
4. **Interceptors**: Middleware for cross-cutting concerns
5. **Load Balancing**: Distributing requests across multiple servers
6. **TLS Security**: Adding encryption for production use
7. **Advanced MarkLogic Features**: Queries, transactions, and semantic operations

## 📚 Additional Resources

- [gRPC Official Documentation](https://grpc.io/)
- [Protocol Buffers Documentation](https://developers.google.com/protocol-buffers)
- [gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)
- [Protocol Buffers Python Tutorial](https://developers.google.com/protocol-buffers/docs/pythontutorial)

## 🤝 Contributing

We welcome contributions! Here are some ways you can help:

### Ideas for Contributions
- Add new RPC methods (UpdateDocument, DeleteDocument, SearchDocuments)
- Implement streaming patterns (server streaming, client streaming, bidirectional)
- Add authentication and authorization examples
- Create more complex message types and nested structures
- Add comprehensive error handling and validation
- Implement TLS/SSL security examples
- Add performance benchmarking tools
- Create Docker containerization examples

### How to Contribute
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup
```bash
# Clone the repository
git clone https://github.com/BillFarber/grpc-protobuf-python-learning.git
cd grpc-protobuf-python-learning

# Install dependencies
pip install -r requirements.txt

# Generate protobuf files
./generate_proto.sh

# Run tests
./marklogic_demo.sh
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Show Your Support

If this project helped you learn gRPC and Protocol Buffers, please give it a star! ⭐

## 🙏 Acknowledgments

- [gRPC Team](https://grpc.io/community/) for the excellent documentation
- [Protocol Buffers Team](https://developers.google.com/protocol-buffers) for the powerful serialization framework
- Python community for the great gRPC tooling

Happy learning! 🎉