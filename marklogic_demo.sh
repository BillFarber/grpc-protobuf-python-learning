#!/bin/bash

# MarkLogic gRPC Service Demonstration Script
echo "🗄️  MarkLogic gRPC Service Demo"
echo "================================"
echo ""

# Start server in background
echo "📡 Starting MarkLogic gRPC server on port 50052..."
SCRIPT_DIR="$(dirname "$0")"
cd "$SCRIPT_DIR/src"
python marklogic_server.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "✅ Server started (PID: $SERVER_PID)"
echo ""

# Test different document insertion scenarios
echo "🔄 Testing document insertion scenarios:"
echo ""

echo "1️⃣ Simple JSON document:"
python -c "
from marklogic_client import insert_document
doc = {'title': 'Hello World', 'type': 'greeting', 'timestamp': '2024-01-01'}
response = insert_document(doc, collections=['greetings'])
print(f'   Status: {response.status_code} - {response.status_message}')
print(f'   URI: {response.document_uri}')
"
echo ""

echo "2️⃣ Complex nested document:"
python -c "
from marklogic_client import insert_document
doc = {
    'customer': {
        'name': 'ACME Corp',
        'id': 12345,
        'orders': [{'id': 1, 'total': 99.99}, {'id': 2, 'total': 149.50}]
    },
    'metadata': {'source': 'demo', 'priority': 'high'}
}
response = insert_document(doc, document_uri='/customers/acme.json', collections=['customers', 'enterprise'])
print(f'   Status: {response.status_code} - {response.status_message}')
print(f'   URI: {response.document_uri}')
"
echo ""

echo "3️⃣ JSON array document:"
python -c "
from marklogic_client import insert_document
doc = [
    {'name': 'Alice', 'role': 'Engineer'},
    {'name': 'Bob', 'role': 'Designer'},
    {'name': 'Charlie', 'role': 'Manager'}
]
response = insert_document(doc, collections=['employees'], metadata={'type': 'staff_list'})
print(f'   Status: {response.status_code} - {response.status_message}')
print(f'   URI: {response.document_uri}')
"
echo ""

echo "4️⃣ Error case - Invalid JSON:"
python -c "
from marklogic_client import insert_document
invalid_json = '{\"name\": \"test\", invalid: }'
response = insert_document(invalid_json)
print(f'   Status: {response.status_code} - {response.status_message}')
print(f'   Details: {response.details}')
"
echo ""

# Stop server
echo "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo "✅ Demo completed!"
echo ""
echo "🚀 To run the services manually:"
echo "   Server: cd src && python marklogic_server.py"
echo "   Client: cd src && python marklogic_client.py"