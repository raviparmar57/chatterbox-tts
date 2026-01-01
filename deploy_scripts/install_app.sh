#!/bin/bash
################################################################################
# Chatterbox TTS - Application Installation Script
# Run this after uploading your application files to /opt/chatterbox-tts
################################################################################

set -e  # Exit on error

echo "=================================================="
echo "Chatterbox TTS - Application Installation"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if in correct directory
if [ ! -f "app.py" ]; then
    print_error "app.py not found. Please run this script from /opt/chatterbox-tts"
    exit 1
fi

print_info "Installing in: $(pwd)"

# Step 1: Create virtual environment
print_info "Step 1: Creating virtual environment..."
python3.11 -m venv venv
print_success "Virtual environment created"

# Step 2: Activate virtual environment
print_info "Step 2: Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Step 3: Upgrade pip
print_info "Step 3: Upgrading pip..."
pip install --upgrade pip setuptools wheel
print_success "Pip upgraded"

# Step 4: Install PyTorch (CPU version)
print_info "Step 4: Installing PyTorch (this may take a while)..."
pip install torch==2.7.1 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cpu
print_success "PyTorch installed"

# Step 5: Install other requirements
print_info "Step 5: Installing other requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Requirements installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Step 6: Test import
print_info "Step 6: Testing imports..."
python -c "import torch; import gradio; import librosa; print('All imports successful')"
print_success "Import test passed"

echo ""
echo "=================================================="
print_success "Application Installation Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Review and edit app_production.py if needed"
echo "2. Run setup_service.sh to create systemd service"
echo ""
