#!/bin/bash

# Script to generate Python code from Protocol Buffer definitions
# This script compiles the .proto files into Python classes

echo "Generating Python code from Protocol Buffer definitions..."

# Get the script directory
SCRIPT_DIR="$(dirname "$0")"

# Generate Python code using the Protocol Buffer compiler
# --python_out: Generate message classes (hello_pb2.py)
# --grpc_python_out: Generate service classes (hello_pb2_grpc.py)
# --proto_path: Path to search for .proto files
# The output goes to the src directory
python -m grpc_tools.protoc \
    --proto_path="$SCRIPT_DIR/proto" \
    --python_out="$SCRIPT_DIR/src" \
    --grpc_python_out="$SCRIPT_DIR/src" \
    hello.proto marklogic.proto

# Check if the generation was successful
if [ $? -eq 0 ]; then
    echo "✅ Successfully generated Python files:"
    echo "   - src/hello_pb2.py (HelloWorld message classes)"
    echo "   - src/hello_pb2_grpc.py (HelloWorld service classes)"
    echo "   - src/marklogic_pb2.py (MarkLogic message classes)"
    echo "   - src/marklogic_pb2_grpc.py (MarkLogic service classes)"
    echo ""
    echo "You can now run the server and client!"
else
    echo "❌ Error generating Python files. Please check your setup."
    exit 1
fi