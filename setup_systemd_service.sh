#!/bin/bash

# Setup systemd service for Chatterbox TTS
# This ensures app runs 24/7 and auto-restarts on failures

echo "Creating systemd service for Chatterbox TTS..."

# Create service file
sudo tee /etc/systemd/system/chatterbox-tts.service > /dev/null <<EOF
[Unit]
Description=Chatterbox TTS - AI Text-to-Speech Service
After=network.target

[Service]
Type=simple
User=centos
Group=centos
WorkingDirectory=/opt/chatterbox-tts/chatterbox-tts
Environment="PATH=/opt/chatterbox-tts/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="GRADIO_SERVER_PORT=7860"
Environment="GRADIO_SERVER_NAME=0.0.0.0"
ExecStart=/opt/chatterbox-tts/venv/bin/python /opt/chatterbox-tts/chatterbox-tts/app_production.py
Restart=always
RestartSec=10
StandardOutput=append:/opt/chatterbox-tts/chatterbox-tts/service.log
StandardError=append:/opt/chatterbox-tts/chatterbox-tts/service_error.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable chatterbox-tts

# Stop any existing nohup processes
pkill -f app_production.py

# Start service
sudo systemctl start chatterbox-tts

# Show status
sudo systemctl status chatterbox-tts

echo ""
echo "============================================"
echo "✅ Systemd service created!"
echo "============================================"
echo ""
echo "Useful commands:"
echo "  Start:   sudo systemctl start chatterbox-tts"
echo "  Stop:    sudo systemctl stop chatterbox-tts"
echo "  Restart: sudo systemctl restart chatterbox-tts"
echo "  Status:  sudo systemctl status chatterbox-tts"
echo "  Logs:    sudo journalctl -u chatterbox-tts -f"
echo ""
echo "Service will:"
echo "  ✅ Start automatically on server boot"
echo "  ✅ Auto-restart if it crashes"
echo "  ✅ Run 24/7 in background"
echo "  ✅ Keep running after you logout"
echo ""
