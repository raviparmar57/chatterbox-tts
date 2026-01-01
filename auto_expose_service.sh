#!/bin/bash

# Auto Expose Service Script
# This script automatically exposes the pod as a service and route
# Runs on VM boot to handle pod name changes

LOG_FILE="/opt/chatterbox-tts/chatterbox-tts/expose.log"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a $LOG_FILE
}

log_message "=========================================="
log_message "🔄 Auto Expose Service Starting..."
log_message "=========================================="

# Wait for network to be ready
sleep 30

# Get current pod name (hostname)
POD_NAME=$(hostname)
log_message "📍 Pod Name: $POD_NAME"

# Check if oc command is available
if ! command -v oc &> /dev/null; then
    log_message "❌ oc command not found"
    log_message "Please install oc CLI: run install_oc_cli.sh"
    exit 0
fi

# Check if logged in
if ! oc whoami &> /dev/null; then
    log_message "❌ Not logged in to OpenShift"
    log_message "Please run: setup_oc_login.sh"
    exit 0
fi

log_message "✅ Logged in as: $(oc whoami)"
log_message "📂 Project: $(oc project -q)"

# Delete old service and route (ignore errors if not exist)
log_message "🗑️  Deleting old service/route..."
oc delete svc chatterbox-tts 2>/dev/null && log_message "   Deleted old service" || log_message "   No old service found"
oc delete route chatterbox-tts 2>/dev/null && log_message "   Deleted old route" || log_message "   No old route found"

# Wait a bit
sleep 5

# Expose current pod as service
log_message "🌐 Exposing pod as service..."
if oc expose pod $POD_NAME --port=7860 --name=chatterbox-tts 2>/dev/null; then
    log_message "✅ Service created successfully"
else
    log_message "⚠️  Service creation failed or already exists"
    # Try to continue anyway
fi

# Wait a bit
sleep 3

# Expose service as route
log_message "🌍 Creating public route..."
if oc expose svc/chatterbox-tts 2>/dev/null; then
    log_message "✅ Route created successfully"
else
    log_message "⚠️  Route creation failed or already exists"
fi

# Get and display the public URL
sleep 2
ROUTE_URL=$(oc get route chatterbox-tts -o jsonpath='{.spec.host}' 2>/dev/null)

if [ -n "$ROUTE_URL" ]; then
    log_message "=========================================="
    log_message "✅ Setup Complete!"
    log_message "=========================================="
    log_message "📍 Public URL: http://$ROUTE_URL"
    log_message ""
else
    log_message "⚠️  Could not retrieve route URL"
    log_message "Check manually with: oc get routes"
fi

log_message "=========================================="
log_message "Auto-expose completed"
log_message "=========================================="
