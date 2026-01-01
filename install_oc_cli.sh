#!/bin/bash

# Install OpenShift CLI (oc) on CentOS
# This enables automation of service/route creation from within the VM

echo "=========================================="
echo "📦 Installing OpenShift CLI (oc)"
echo "=========================================="
echo ""

# Create temp directory
mkdir -p /tmp/oc-install
cd /tmp/oc-install

# Download oc CLI for Linux
echo "⬇️  Downloading oc CLI..."
curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-linux.tar.gz

if [ $? -ne 0 ]; then
    echo "❌ Download failed. Trying alternative mirror..."
    curl -LO https://downloads-openshift-console.apps.rm2.thpm.p1.openshiftapps.com/amd64/linux/oc.tar
fi

# Extract
echo "📂 Extracting..."
tar -xzf openshift-client-linux.tar.gz 2>/dev/null || tar -xf oc.tar 2>/dev/null

# Move to /usr/local/bin
echo "📁 Installing to /usr/local/bin..."
sudo mv oc kubectl /usr/local/bin/ 2>/dev/null || sudo mv oc /usr/local/bin/

# Make executable
sudo chmod +x /usr/local/bin/oc

# Cleanup
cd ~
rm -rf /tmp/oc-install

# Verify installation
echo ""
echo "=========================================="
echo "✅ Verifying Installation"
echo "=========================================="

if command -v oc &> /dev/null; then
    echo "✅ oc CLI installed successfully!"
    echo ""
    oc version --client
    echo ""
else
    echo "❌ Installation failed!"
    exit 1
fi

echo "=========================================="
echo "📋 Next Steps:"
echo "=========================================="
echo ""
echo "1. Login to OpenShift:"
echo "   oc login --token=<your-token> --server=https://api.rm2.thpm.p1.openshiftapps.com:6443"
echo ""
echo "2. Get your token from:"
echo "   OpenShift Console → Your Name → Copy Login Command"
echo ""
echo "3. After login, the auto-expose service will work automatically!"
echo ""
