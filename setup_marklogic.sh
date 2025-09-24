#!/bin/bash

# MarkLogic Environment Setup Script
# This script helps configure the environment for MarkLogic integration

echo "🔧 MarkLogic gRPC Integration Setup"
echo "=================================="
echo ""

# Check if MarkLogic Python client is installed
echo "📋 Checking dependencies..."
python -c "import marklogic; print('✅ MarkLogic Python client is installed')" 2>/dev/null || {
    echo "❌ MarkLogic Python client not found"
    echo "📦 Installing MarkLogic Python client..."
    pip install marklogic==1.4.0
    if [ $? -eq 0 ]; then
        echo "✅ MarkLogic Python client installed successfully"
    else
        echo "❌ Failed to install MarkLogic Python client"
        exit 1
    fi
}

echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env file with your MarkLogic server details"
    echo ""
    echo "Default configuration:"
    echo "  Host: localhost"
    echo "  Port: 8000"
    echo "  Username: admin"
    echo "  Password: admin"
    echo "  Database: Documents"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "📋 Current MarkLogic configuration:"
    echo "  Host: ${MARKLOGIC_HOST:-localhost}"
    echo "  Port: ${MARKLOGIC_PORT:-8000}"
    echo "  Database: ${MARKLOGIC_DATABASE:-Documents}"
    echo "  Username: ${MARKLOGIC_USERNAME:-admin}"
    echo ""
fi

echo "🚀 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Ensure MarkLogic server is running"
echo "2. Edit .env file if needed"
echo "3. Run: ./marklogic_demo.sh"
echo ""
echo "The gRPC server will automatically:"
echo "• Try to connect to MarkLogic using .env settings"
echo "• Fall back to simulation mode if connection fails"
echo "• Show connection status in the server logs"