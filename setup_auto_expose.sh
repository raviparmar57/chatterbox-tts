#!/bin/bash

# Setup Auto Expose Service
# This creates a systemd service that runs on boot to automatically
# expose the pod as a service and route

echo "=========================================="
echo "🚀 Auto Expose Service Setup"
echo "=========================================="
echo ""

# Make sure the script is executable
chmod +x /opt/chatterbox-tts/chatterbox-tts/auto_expose_service.sh

# Create systemd service
echo "📝 Creating systemd service..."
sudo tee /etc/systemd/system/chatterbox-auto-expose.service > /dev/null <<'EOF'
[Unit]
Description=Chatterbox Auto Expose OpenShift Service
After=network-online.target chatterbox-tts.service
Wants=network-online.target

[Service]
Type=oneshot
User=centos
Group=centos
WorkingDirectory=/opt/chatterbox-tts/chatterbox-tts
ExecStart=/opt/chatterbox-tts/chatterbox-tts/auto_expose_service.sh
RemainAfterExit=true
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable service to run on boot
echo "✅ Enabling auto-expose service..."
sudo systemctl enable chatterbox-auto-expose

# Start service now (for testing)
echo "🚀 Starting service..."
sudo systemctl start chatterbox-auto-expose

# Wait a moment
sleep 5

# Show status
echo ""
echo "=========================================="
echo "📊 Service Status:"
echo "=========================================="
sudo systemctl status chatterbox-auto-expose --no-pager

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📋 What This Does:"
echo "  ✅ Runs automatically on VM boot"
echo "  ✅ Gets current pod name"
echo "  ✅ Deletes old service/route"
echo "  ✅ Creates new service/route"
echo "  ✅ Works even when pod name changes"
echo ""
echo "📋 Commands:"
echo "  Status:  sudo systemctl status chatterbox-auto-expose"
echo "  Logs:    sudo journalctl -u chatterbox-auto-expose -f"
echo "  Restart: sudo systemctl restart chatterbox-auto-expose"
echo "  Disable: sudo systemctl disable chatterbox-auto-expose"
echo ""
echo "🧪 Test Now:"
echo "  sudo systemctl restart chatterbox-auto-expose"
echo "  oc get routes"
echo ""
