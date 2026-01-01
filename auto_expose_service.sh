#!/bin/bash

# Auto Expose Service Script
# This script automatically exposes the pod as a service and route
# Runs on VM boot to handle pod name changes

echo "=========================================="
echo "🔄 Auto Expose Service Starting..."
echo "=========================================="

# Wait for network to be ready
sleep 30

# Get current pod name (hostname)
POD_NAME=$(hostname)
echo "📍 Pod Name: $POD_NAME"

# Check if oc command is available
if ! command -v oc &> /dev/null; then
    echo "❌ oc command not found"
    echo "Skipping OpenShift service creation"
    exit 0
fi

# Login to OpenShift (using token from environment or config)
# oc login is usually already configured in the pod

# Delete old service and route (ignore errors if not exist)
echo "🗑️  Deleting old service/route..."
oc delete svc chatterbox-tts 2>/dev/null || echo "No old service found"
oc delete route chatterbox-tts 2>/dev/null || echo "No old route found"

# Wait a bit
sleep 5

# Expose current pod as service
echo "🌐 Exposing pod as service..."
oc expose pod $POD_NAME --port=7860 --name=chatterbox-tts 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Service created successfully"
else
    echo "⚠️  Service creation failed or already exists"
fi

# Wait a bit
sleep 3

# Expose service as route
echo "🌍 Creating public route..."
oc expose svc/chatterbox-tts 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Route created successfully"
else
    echo "⚠️  Route creation failed or already exists"
fi

# Get and display the public URL
sleep 2
ROUTE_URL=$(oc get route chatterbox-tts -o jsonpath='{.spec.host}' 2>/dev/null)

if [ -n "$ROUTE_URL" ]; then
    echo ""
    echo "=========================================="
    echo "✅ Setup Complete!"
    echo "=========================================="
    echo "📍 Public URL: http://$ROUTE_URL"
    echo ""
else
    echo ""
    echo "⚠️  Could not retrieve route URL"
    echo "Check manually with: oc get routes"
fi

# Log to file
echo "$(date): Service exposed for pod $POD_NAME" >> /opt/chatterbox-tts/chatterbox-tts/expose.log
