#!/bin/bash
################################################################################
# Chatterbox TTS - CentOS VPS Setup Script
# This script automates the initial setup on a fresh CentOS/RHEL VPS
################################################################################

set -e  # Exit on error

echo "=================================================="
echo "Chatterbox TTS - VPS Setup Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run this script as root. Use a regular user with sudo privileges."
    exit 1
fi

# Step 1: Update system
print_info "Step 1: Updating system packages..."
sudo dnf update -y
sudo dnf upgrade -y
print_success "System updated"

# Step 2: Install basic tools
print_info "Step 2: Installing basic tools..."
sudo dnf install -y git wget curl vim nano htop
print_success "Basic tools installed"

# Step 3: Install Python 3.11
print_info "Step 3: Installing Python 3.11..."
sudo dnf install -y epel-release
sudo dnf install -y python3.11 python3.11-pip python3.11-devel

# Verify Python installation
if command -v python3.11 &> /dev/null; then
    PYTHON_VERSION=$(python3.11 --version)
    print_success "Python installed: $PYTHON_VERSION"
else
    print_error "Python 3.11 installation failed"
    exit 1
fi

# Step 4: Install system dependencies
print_info "Step 4: Installing system dependencies for audio processing..."
sudo dnf install -y \
    libsndfile \
    ffmpeg \
    sox \
    portaudio-devel \
    alsa-lib-devel \
    gcc \
    gcc-c++ \
    make
print_success "System dependencies installed"

# Step 5: Create application directory
print_info "Step 5: Creating application directory..."
sudo mkdir -p /opt/chatterbox-tts
sudo chown $USER:$USER /opt/chatterbox-tts
print_success "Application directory created at /opt/chatterbox-tts"

# Step 6: Install Nginx
print_info "Step 6: Installing Nginx..."
sudo dnf install -y nginx
sudo systemctl enable nginx
print_success "Nginx installed"

# Step 7: Configure firewall
print_info "Step 7: Configuring firewall..."
sudo systemctl enable firewalld
sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-port=7860/tcp
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
print_success "Firewall configured"

# Step 8: Create log directory
print_info "Step 8: Creating log directory..."
sudo mkdir -p /var/log/chatterbox-tts
sudo chown $USER:$USER /var/log/chatterbox-tts
print_success "Log directory created"

# Step 9: Install Certbot (for SSL)
print_info "Step 9: Installing Certbot for SSL..."
sudo dnf install -y certbot python3-certbot-nginx
print_success "Certbot installed"

echo ""
echo "=================================================="
print_success "VPS Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Upload your application files to /opt/chatterbox-tts"
echo "2. Run the install_app.sh script to set up the application"
echo ""
print_info "You can upload files using:"
echo "   scp -r /local/path/* $USER@$(hostname -I | awk '{print $1}'):/opt/chatterbox-tts/"
echo ""
