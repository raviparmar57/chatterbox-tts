#!/bin/bash

# Setup OpenShift Login for Auto-Reconnect
# This script helps you configure persistent OpenShift authentication

echo "=========================================="
echo "🔐 OpenShift Login Setup"
echo "=========================================="
echo ""

echo "To get your login token:"
echo ""
echo "1. Go to OpenShift Console in browser"
echo "2. Click your name (top right)"
echo "3. Click 'Copy login command'"
echo "4. Click 'Display Token'"
echo "5. Copy the 'oc login' command"
echo ""
echo "Paste the full 'oc login' command below:"
echo "(Example: oc login --token=sha256~xxxxx --server=https://api...)"
echo ""

read -p "Paste login command: " LOGIN_CMD

# Execute login
eval $LOGIN_CMD

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Login successful!"
    echo ""
    
    # Set default project
    echo "Setting default project..."
    oc project casabor968-dev
    
    echo ""
    echo "=========================================="
    echo "✅ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Your login credentials are saved."
    echo "The auto-expose service will now work automatically on boot!"
    echo ""
    
    # Test the auto-expose script
    echo "Testing auto-expose script..."
    /opt/chatterbox-tts/chatterbox-tts/auto_expose_service.sh
    
else
    echo ""
    echo "❌ Login failed!"
    echo "Please check your token and try again."
    exit 1
fi
