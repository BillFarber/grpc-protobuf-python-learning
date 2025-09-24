#!/bin/bash

# Script to run the complete gRPC HelloWorld example
# This script will generate the protobuf files, start the server, and run the client

echo "🚀 Running gRPC HelloWorld Example"
echo "=================================="

# Step 1: Generate Protocol Buffer files
echo ""
echo "Step 1: Generating Protocol Buffer files..."
./generate_proto.sh

if [ $? -ne 0 ]; then
    echo "❌ Failed to generate protobuf files. Exiting."
    exit 1
fi

# Step 2: Start the server in the background
echo ""
echo "Step 2: Starting the gRPC server..."
cd src
python server.py &
SERVER_PID=$!

# Give the server a moment to start up
sleep 2

# Check if the server is still running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ Server failed to start. Exiting."
    exit 1
fi

echo "✅ Server started successfully (PID: $SERVER_PID)"

# Step 3: Run the client
echo ""
echo "Step 3: Running the client..."
echo "Press Ctrl+C to stop the server when done."
echo ""

# Run the client
python client.py

# Step 4: Clean up - stop the server
echo ""
echo "Step 4: Stopping the server..."
kill $SERVER_PID 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Server stopped successfully"
else
    echo "⚠️  Server may have already stopped"
fi

echo ""
echo "🎉 Example completed!"