#!/bin/bash
################################################################################
# Chatterbox TTS - Nginx Configuration Script
################################################################################

set -e

echo "=================================================="
echo "Chatterbox TTS - Nginx Configuration"
echo "=================================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

print_question() {
    echo -e "${BLUE}? $1${NC}"
}

# Ask for domain or IP
print_question "Enter your domain name (e.g., example.com) or VPS IP address:"
read -r SERVER_NAME

if [ -z "$SERVER_NAME" ]; then
    echo "No domain/IP provided. Exiting."
    exit 1
fi

print_info "Configuring Nginx for: $SERVER_NAME"

# Create Nginx configuration
cat > /tmp/chatterbox-tts.conf << EOF
upstream gradio_backend {
    server 127.0.0.1:7860;
}

server {
    listen 80;
    server_name $SERVER_NAME;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://gradio_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout 600s;
    }
    
    location /api {
        proxy_pass http://gradio_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }
}
EOF

# Move to Nginx directory
sudo mv /tmp/chatterbox-tts.conf /etc/nginx/conf.d/

print_success "Nginx configuration created"

# Test configuration
print_info "Testing Nginx configuration..."
sudo nginx -t

# Restart Nginx
print_info "Restarting Nginx..."
sudo systemctl restart nginx

print_success "Nginx configured and restarted"

echo ""
echo "=================================================="
print_success "Nginx Setup Complete!"
echo "=================================================="
echo ""
echo "Your application should be accessible at:"
echo "  http://$SERVER_NAME"
echo ""
print_info "To enable HTTPS, run:"
echo "  sudo certbot --nginx -d $SERVER_NAME"
echo ""
