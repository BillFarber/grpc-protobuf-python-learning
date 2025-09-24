#!/bin/bash

# Simple demonstration script
echo "🚀 gRPC HelloWorld Demonstration"
echo "================================"
echo ""

# Start server in background
echo "📡 Starting gRPC server..."
cd /Users/pbarber/Documents/Sandboxes/gRPC/grpc-hello-world/src
python server.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

echo "✅ Server started (PID: $SERVER_PID)"
echo ""

# Test with different names
echo "🔄 Testing client with different names:"
echo ""

for name in "World" "Alice" "Bob" "Python Developer"; do
    echo "Testing with name: $name"
    python -c "
from client import run_client
result = run_client('$name')
if result:
    print('✅ Success:', result)
else:
    print('❌ Failed')
"
    echo ""
done

# Stop server
echo "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo "✅ Demonstration complete!"
echo ""
echo "To run manually:"
echo "1. Terminal 1: cd src && python server.py"
echo "2. Terminal 2: cd src && python client.py"