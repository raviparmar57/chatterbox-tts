#!/bin/bash
################################################################################
# Chatterbox TTS - Systemd Service Setup Script
################################################################################

set -e

echo "=================================================="
echo "Chatterbox TTS - Service Setup"
echo "=================================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Get current user
CURRENT_USER=$(whoami)
APP_DIR="/opt/chatterbox-tts"

print_info "Creating systemd service for user: $CURRENT_USER"

# Create service file
cat > /tmp/chatterbox-tts.service << EOF
[Unit]
Description=Chatterbox TTS Enhanced Service
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/python app_production.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/chatterbox-tts/output.log
StandardError=append:/var/log/chatterbox-tts/error.log

# Resource limits
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

# Move to systemd directory
sudo mv /tmp/chatterbox-tts.service /etc/systemd/system/

print_success "Service file created"

# Reload systemd
print_info "Reloading systemd..."
sudo systemctl daemon-reload

# Enable service
print_info "Enabling service..."
sudo systemctl enable chatterbox-tts.service

print_success "Service enabled"

echo ""
echo "=================================================="
print_success "Service Setup Complete!"
echo "=================================================="
echo ""
echo "Control the service with:"
echo "  sudo systemctl start chatterbox-tts    # Start"
echo "  sudo systemctl stop chatterbox-tts     # Stop"
echo "  sudo systemctl restart chatterbox-tts  # Restart"
echo "  sudo systemctl status chatterbox-tts   # Status"
echo ""
echo "View logs with:"
echo "  sudo journalctl -u chatterbox-tts -f"
echo ""
