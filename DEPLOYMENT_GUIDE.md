# Deployment Guide: Chatterbox TTS on CentOS VPS (Red Hat Developer Sandbox)

This guide provides step-by-step instructions to deploy the Chatterbox TTS application on a CentOS/RHEL VPS using Gradio API.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial VPS Setup](#initial-vps-setup)
3. [Install Python and Dependencies](#install-python-and-dependencies)
4. [Clone and Setup Application](#clone-and-setup-application)
5. [Configure Application for Production](#configure-application-for-production)
6. [Setup Systemd Service](#setup-systemd-service)
7. [Configure Firewall](#configure-firewall)
8. [Setup Nginx Reverse Proxy (Optional but Recommended)](#setup-nginx-reverse-proxy)
9. [SSL/TLS Configuration](#ssltls-configuration)
10. [Gradio API Usage](#gradio-api-usage)
11. [Monitoring and Maintenance](#monitoring-and-maintenance)
12. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:
- Access to a CentOS/RHEL VPS (Red Hat Developer Sandbox)
- SSH access to the VPS
- Root or sudo privileges
- At least 4GB RAM (8GB+ recommended for ML models)
- At least 20GB disk space
- Domain name (optional, for SSL/TLS)

---

## 1. Initial VPS Setup

### Step 1.1: Connect to Your VPS
```bash
ssh username@your-vps-ip
```

### Step 1.2: Update System Packages
```bash
sudo dnf update -y
sudo dnf upgrade -y
```

### Step 1.3: Install Basic Tools
```bash
sudo dnf install -y git wget curl vim nano htop
```

---

## 2. Install Python and Dependencies

### Step 2.1: Install Python 3.10 or 3.11
CentOS/RHEL may have older Python versions. Install Python 3.10+:

```bash
# Enable EPEL repository
sudo dnf install -y epel-release

# Install Python 3.11
sudo dnf install -y python3.11 python3.11-pip python3.11-devel

# Verify installation
python3.11 --version
```

**Alternative: Install from source if not available**
```bash
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y openssl-devel bzip2-devel libffi-devel zlib-devel

cd /tmp
wget https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz
tar xzf Python-3.11.7.tgz
cd Python-3.11.7
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Verify
python3.11 --version
```

### Step 2.2: Install System Dependencies for Audio Processing
```bash
sudo dnf install -y \
    libsndfile \
    ffmpeg \
    sox \
    portaudio-devel \
    alsa-lib-devel
```

### Step 2.3: Install PyTorch Dependencies (for CPU or GPU)

**For CPU-only deployment:**
```bash
# Already handled in requirements.txt
```

**For GPU deployment (if you have NVIDIA GPU):**
```bash
# Install NVIDIA drivers and CUDA toolkit
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo
sudo dnf install -y cuda-toolkit-12-1
sudo dnf install -y nvidia-driver

# Verify
nvidia-smi
```

---

## 3. Clone and Setup Application

### Step 3.1: Create Application Directory
```bash
sudo mkdir -p /opt/chatterbox-tts
sudo chown $USER:$USER /opt/chatterbox-tts
cd /opt/chatterbox-tts
```

### Step 3.2: Clone/Upload Your Application
**Option A: Using Git (if you have a repository)**
```bash
git clone <your-repo-url> .
```

**Option B: Upload via SCP from local machine**
```bash
# Run this from your local machine
scp -r /path/to/chatterbox-tts/* username@your-vps-ip:/opt/chatterbox-tts/
```

**Option C: Using rsync (more efficient)**
```bash
# Run this from your local machine
rsync -avz --progress /path/to/chatterbox-tts/ username@your-vps-ip:/opt/chatterbox-tts/
```

### Step 3.3: Create Virtual Environment
```bash
cd /opt/chatterbox-tts
python3.11 -m venv venv
source venv/bin/activate
```

### Step 3.4: Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

### Step 3.5: Install Python Dependencies
```bash
# Install PyTorch first (CPU version for Red Hat)
pip install torch==2.7.1 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cpu

# Install other requirements
pip install -r requirements.txt
```

**Note:** If you encounter any installation errors, you may need to install packages one by one or adjust versions.

---

## 4. Configure Application for Production

### Step 4.1: Create Production Configuration File
Create a new file `app_production.py`:

```bash
nano app_production.py
```

Add the following content:

```python
"""
Chatterbox TTS Enhanced - Production Deployment
"""
import sys
import os

# Add src directory and project root to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

import gradio as gr
from modules.config import LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
from modules.voice_manager import (
    load_voices, 
    get_voices_for_language, 
    get_all_voices_with_gender,
    resolve_voice_path,
    clone_voice,
    delete_voice
)
from modules.generation_functions import (
    generate_speech,
    generate_multilingual_speech,
    convert_voice
)

# Import UI components
from modules.ui_components import (
    create_header,
    create_tts_tab,
    create_multilingual_tab,
    create_voice_conversion_tab,
    create_clone_voice_tab
)

# Load voices at startup
available_voices = load_voices()

# ---------------------------
# Main Application
# ---------------------------
with gr.Blocks(title="Chatterbox TTS Enhanced", theme=gr.themes.Soft()) as demo:
    # State variables
    tts_model_state = gr.State(None)
    vc_model_state = gr.State(None)
    mtl_model_state = gr.State(None)
    
    # Header
    create_header()
    
    # Create tabs
    with gr.Tab("🎤 Text-to-Speech"):
        tts_components = create_tts_tab()
    
    with gr.Tab("🌍 Multilingual TTS"):
        mtl_components = create_multilingual_tab()
    
    with gr.Tab("🔄 Voice Conversion"):
        vc_components = create_voice_conversion_tab()
    
    with gr.Tab("🧬 Clone Voice"):
        clone_components = create_clone_voice_tab()
    
    # ---------------------------
    # Event Handlers - TTS Tab
    # ---------------------------
    tts_components['generate_btn'].click(
        fn=generate_speech,
        inputs=[
            tts_components['text'],
            tts_components['voice_select'],
            tts_components['exaggeration'],
            tts_components['temp'],
            tts_components['seed_num'],
            tts_components['cfg_weight'],
            tts_components['min_p'],
            tts_components['top_p'],
            tts_components['repetition_penalty']
        ],
        outputs=[
            tts_components['progress_bar'],
            tts_components['audio_output'],
            tts_components['status_box']
        ]
    )
    
    # Update preview when voice changes
    def update_tts_preview(voice_name):
        path = resolve_voice_path(voice_name, "en")
        return path

    tts_components['voice_select'].change(
        fn=update_tts_preview,
        inputs=[tts_components['voice_select']],
        outputs=[tts_components['preview_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Multilingual Tab
    # ---------------------------
    mtl_components['generate_btn'].click(
        fn=generate_multilingual_speech,
        inputs=[
            mtl_components['text'],
            mtl_components['voice_select'],
            mtl_components['language_select'],
            mtl_components['exaggeration'],
            mtl_components['temp'],
            mtl_components['seed_num'],
            mtl_components['cfg_weight']
        ],
        outputs=[
            mtl_components['progress_bar'],
            mtl_components['audio_output'],
            mtl_components['status_box']
        ]
    )
    
    # Update language change
    mtl_components['language_select'].change(
        fn=lambda lang: (
            LANGUAGE_CONFIG.get(lang, {}).get("text", ""),
            gr.update(choices=get_voices_for_language(lang), value=f"Default ({SUPPORTED_LANGUAGES.get(lang, lang)})")
        ),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['text'], mtl_components['voice_select']]
    )
    
    # Update preview when voice changes (Multilingual)
    def update_mtl_preview(voice_name, language_code):
        path = resolve_voice_path(voice_name, language_code)
        return path

    mtl_components['voice_select'].change(
        fn=update_mtl_preview,
        inputs=[mtl_components['voice_select'], mtl_components['language_select']],
        outputs=[mtl_components['sample_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Voice Conversion Tab
    # ---------------------------
    vc_components['convert_btn'].click(
        fn=convert_voice,
        inputs=[vc_components['input_audio'], vc_components['target_voice_select']],
        outputs=[vc_components['progress_bar'], vc_components['audio_output'], vc_components['status_box']]
    )
    
    # Update preview when voice changes (VC)
    def update_vc_preview(voice_name):
        if voice_name == "None": 
            return None
        
        # Remove gender symbols if present
        clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        # Check if it's a default voice string like "Default (English)"
        if clean_name.startswith("Default ("):
            # Extract language name
            lang_name = clean_name.split("(")[1].split(")")[0]
            # Find code
            for code, name in SUPPORTED_LANGUAGES.items():
                if name == lang_name:
                    return LANGUAGE_CONFIG.get(code, {}).get("audio")
        
        # Try different possible names with gender suffixes
        from modules.voice_manager import VOICES
        possible_names = [
            clean_name,
            f"{clean_name}_male",
            f"{clean_name}_female"
        ]
        
        # Check cloned voices
        for name in possible_names:
            if name in VOICES["samples"]:
                return VOICES["samples"][name]
        
        # Try finding it with language suffixes if not found directly
        for code in SUPPORTED_LANGUAGES:
            for name in possible_names:
                full_name = f"{name}_{code}"
                if full_name in VOICES["samples"]:
                    return VOICES["samples"][full_name]
        
        return None

    vc_components['target_voice_select'].change(
        fn=update_vc_preview,
        inputs=[vc_components['target_voice_select']],
        outputs=[vc_components['preview_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Clone Voice Tab
    # ---------------------------
    # Update all voice dropdowns when cloning
    clone_components['clone_btn'].click(
        fn=clone_voice,
        inputs=[
            clone_components['ref_audio_input'],
            clone_components['new_voice_name'],
            clone_components['voice_language'],
            clone_components['voice_gender']
        ],
        outputs=[clone_components['clone_status'], tts_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[tts_components['voice_select']]
    ).then(
        fn=lambda lang: gr.update(choices=get_voices_for_language(lang)),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender()),
        outputs=[vc_components['target_voice_select']]
    ).then(
        fn=lambda: "\n".join(load_voices()) if load_voices() else "No voices cloned yet",
        outputs=[clone_components['current_voices_display']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender(), value="None"),
        outputs=[clone_components['voice_to_delete']]
    )
    
    # Delete voice functionality in Clone Voice tab
    clone_components['delete_btn'].click(
        fn=delete_voice,
        inputs=[clone_components['voice_to_delete']],
        outputs=[clone_components['delete_status'], clone_components['voice_to_delete']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[tts_components['voice_select']]
    ).then(
        fn=lambda lang: gr.update(choices=get_voices_for_language(lang)),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender()),
        outputs=[vc_components['target_voice_select']]
    ).then(
        fn=lambda: "\n".join(load_voices()) if load_voices() else "No voices cloned yet",
        outputs=[clone_components['current_voices_display']]
    )


if __name__ == "__main__":
    # Production configuration
    demo.queue(
        max_size=50,
        default_concurrency_limit=5,  # Adjust based on your server capacity
    ).launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=7860,  # Default Gradio port
        share=False,  # Disable public sharing
        show_error=True,
        enable_queue=True,
        auth=None,  # Add authentication: auth=("username", "password")
        # For API access, set:
        show_api=True,  # Enable API documentation
        api_open=True,  # Allow API access
    )
```

Save and exit (Ctrl+X, then Y, then Enter).

### Step 4.2: Test the Application
```bash
source venv/bin/activate
python app_production.py
```

If it starts successfully, press Ctrl+C to stop it. We'll set up a proper service next.

---

## 5. Setup Systemd Service

### Step 5.1: Create Systemd Service File
```bash
sudo nano /etc/systemd/system/chatterbox-tts.service
```

Add the following content:

```ini
[Unit]
Description=Chatterbox TTS Enhanced Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/chatterbox-tts
Environment="PATH=/opt/chatterbox-tts/venv/bin"
ExecStart=/opt/chatterbox-tts/venv/bin/python app_production.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/chatterbox-tts/output.log
StandardError=append:/var/log/chatterbox-tts/error.log

# Resource limits (adjust based on your VPS)
LimitNOFILE=65536
MemoryLimit=6G

[Install]
WantedBy=multi-user.target
```

**Replace `your-username` with your actual username.**

### Step 5.2: Create Log Directory
```bash
sudo mkdir -p /var/log/chatterbox-tts
sudo chown $USER:$USER /var/log/chatterbox-tts
```

### Step 5.3: Reload Systemd and Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable chatterbox-tts.service
sudo systemctl start chatterbox-tts.service
```

### Step 5.4: Check Service Status
```bash
sudo systemctl status chatterbox-tts.service
```

### Step 5.5: View Logs
```bash
# Real-time logs
sudo journalctl -u chatterbox-tts.service -f

# View output log
tail -f /var/log/chatterbox-tts/output.log

# View error log
tail -f /var/log/chatterbox-tts/error.log
```

---

## 6. Configure Firewall

### Step 6.1: Enable Firewalld
```bash
sudo systemctl enable firewalld
sudo systemctl start firewalld
```

### Step 6.2: Open Required Ports
```bash
# Open Gradio default port (7860)
sudo firewall-cmd --permanent --add-port=7860/tcp

# If using Nginx (HTTP and HTTPS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Reload firewall
sudo firewall-cmd --reload

# Verify
sudo firewall-cmd --list-all
```

---

## 7. Setup Nginx Reverse Proxy (Optional but Recommended)

Using Nginx provides better security, SSL/TLS support, and load balancing capabilities.

### Step 7.1: Install Nginx
```bash
sudo dnf install -y nginx
```

### Step 7.2: Configure Nginx
```bash
sudo nano /etc/nginx/conf.d/chatterbox-tts.conf
```

Add the following configuration:

```nginx
upstream gradio_backend {
    server 127.0.0.1:7860;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # Replace with your domain or VPS IP
    
    # Redirect HTTP to HTTPS (after SSL setup)
    # return 301 https://$server_name$request_uri;
    
    client_max_body_size 100M;  # For audio file uploads
    
    location / {
        proxy_pass http://gradio_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for long-running requests
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout 600s;
    }
    
    # API endpoint
    location /api {
        proxy_pass http://gradio_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }
}
```

**Replace `your-domain.com` with your actual domain or VPS IP address.**

### Step 7.3: Test Nginx Configuration
```bash
sudo nginx -t
```

### Step 7.4: Enable and Start Nginx
```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

### Step 7.5: Update Firewall (if needed)
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 8. SSL/TLS Configuration

### Step 8.1: Install Certbot
```bash
sudo dnf install -y certbot python3-certbot-nginx
```

### Step 8.2: Obtain SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts and choose to redirect HTTP to HTTPS.

### Step 8.3: Auto-Renewal Setup
Certbot automatically sets up a cron job. Verify:

```bash
sudo systemctl list-timers | grep certbot
```

Test renewal:
```bash
sudo certbot renew --dry-run
```

---

## 9. Gradio API Usage

### 9.1: Access API Documentation
Once deployed, access the API documentation at:
```
http://your-domain.com/api/docs
```
or
```
http://your-vps-ip:7860/api/docs
```

### 9.2: Python Client Example

Create a test script `test_api.py`:

```python
from gradio_client import Client

# Connect to your deployed instance
client = Client("http://your-domain.com")  # or "http://your-vps-ip:7860"

# Example 1: Text-to-Speech
result = client.predict(
    text="Hello, this is a test of the TTS system.",
    voice_select="Morgan Freeman_male",
    exaggeration=1.0,
    temp=0.7,
    seed_num=42,
    cfg_weight=1.0,
    min_p=0.1,
    top_p=0.9,
    repetition_penalty=1.0,
    api_name="/generate_speech"  # Check API docs for exact endpoint name
)

print(f"Generated audio: {result}")

# Example 2: Multilingual TTS
result = client.predict(
    text="Bonjour, comment allez-vous?",
    voice_select="Default (French)",
    language_select="fr",
    exaggeration=1.0,
    temp=0.7,
    seed_num=42,
    cfg_weight=1.0,
    api_name="/generate_multilingual"
)

print(f"Generated audio: {result}")
```

### 9.3: cURL Example

```bash
# Get API info
curl http://your-domain.com/api/

# Make API request (example - adjust based on actual API)
curl -X POST http://your-domain.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      "Hello world",
      "Morgan Freeman_male",
      1.0,
      0.7,
      42,
      1.0,
      0.1,
      0.9,
      1.0
    ]
  }'
```

### 9.4: JavaScript/Node.js Example

```javascript
const { Client } = require("@gradio/client");

async function generateSpeech() {
  const client = await Client.connect("http://your-domain.com");
  
  const result = await client.predict("/generate_speech", {
    text: "Hello from JavaScript!",
    voice_select: "Morgan Freeman_male",
    exaggeration: 1.0,
    temp: 0.7,
    seed_num: 42,
    cfg_weight: 1.0,
    min_p: 0.1,
    top_p: 0.9,
    repetition_penalty: 1.0
  });
  
  console.log("Generated audio:", result.data);
}

generateSpeech();
```

---

## 10. Monitoring and Maintenance

### 10.1: System Monitoring

**Monitor service status:**
```bash
sudo systemctl status chatterbox-tts.service
```

**Monitor resource usage:**
```bash
htop
# or
top
```

**Monitor disk space:**
```bash
df -h
```

**Monitor logs:**
```bash
# Application logs
tail -f /var/log/chatterbox-tts/output.log
tail -f /var/log/chatterbox-tts/error.log

# System logs
sudo journalctl -u chatterbox-tts.service -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 10.2: Restart Service
```bash
sudo systemctl restart chatterbox-tts.service
```

### 10.3: Update Application
```bash
cd /opt/chatterbox-tts
source venv/bin/activate

# Pull latest changes (if using Git)
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart chatterbox-tts.service
```

### 10.4: Backup

**Create backup script:**
```bash
nano ~/backup_chatterbox.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/backup/chatterbox-tts"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup application
tar -czf $BACKUP_DIR/chatterbox_app_$DATE.tar.gz /opt/chatterbox-tts

# Backup logs
tar -czf $BACKUP_DIR/chatterbox_logs_$DATE.tar.gz /var/log/chatterbox-tts

# Keep only last 7 backups
find $BACKUP_DIR -name "chatterbox_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable:
```bash
chmod +x ~/backup_chatterbox.sh
```

Schedule with cron:
```bash
crontab -e
```

Add:
```
0 2 * * * /home/your-username/backup_chatterbox.sh
```

---

## 11. Troubleshooting

### Issue 1: Service Won't Start
```bash
# Check logs
sudo journalctl -u chatterbox-tts.service -n 50 --no-pager

# Check if port is in use
sudo netstat -tulpn | grep 7860

# Check permissions
ls -la /opt/chatterbox-tts
```

### Issue 2: Out of Memory
```bash
# Check memory usage
free -h

# Reduce concurrency in app_production.py:
# default_concurrency_limit=1  # Instead of 5

# Add swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Issue 3: Slow Performance
- Reduce `default_concurrency_limit` in `app_production.py`
- Use CPU optimizations for PyTorch
- Consider upgrading VPS resources

### Issue 4: Connection Refused
```bash
# Check if service is running
sudo systemctl status chatterbox-tts.service

# Check firewall
sudo firewall-cmd --list-all

# Check if Nginx is running
sudo systemctl status nginx

# Test local connection
curl http://localhost:7860
```

### Issue 5: Model Loading Issues
```bash
# Check if models are downloaded
ls -la /opt/chatterbox-tts/checkpoints/

# Check disk space
df -h

# Check logs for specific errors
tail -f /var/log/chatterbox-tts/error.log
```

---

## 12. Security Best Practices

### 12.1: Enable Authentication
Edit `app_production.py`:
```python
demo.launch(
    ...
    auth=("admin", "your_secure_password"),  # Add authentication
    ...
)
```

### 12.2: Use HTTPS Only
After SSL setup, enforce HTTPS in Nginx config.

### 12.3: Rate Limiting
Add to Nginx config:
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api {
    limit_req zone=api_limit burst=20 nodelay;
    ...
}
```

### 12.4: Fail2Ban (Optional)
```bash
sudo dnf install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 12.5: Regular Updates
```bash
# System updates
sudo dnf update -y

# Python package updates
cd /opt/chatterbox-tts
source venv/bin/activate
pip list --outdated
pip install --upgrade <package_name>
```

---

## Quick Reference Commands

```bash
# Start service
sudo systemctl start chatterbox-tts.service

# Stop service
sudo systemctl stop chatterbox-tts.service

# Restart service
sudo systemctl restart chatterbox-tts.service

# Check status
sudo systemctl status chatterbox-tts.service

# View logs
sudo journalctl -u chatterbox-tts.service -f

# Restart Nginx
sudo systemctl restart nginx

# Test Nginx config
sudo nginx -t

# Check application URL
curl http://localhost:7860
```

---

## Summary

You now have:
1. ✅ CentOS VPS configured with Python and dependencies
2. ✅ Chatterbox TTS application deployed
3. ✅ Systemd service for auto-start and management
4. ✅ Nginx reverse proxy for better performance
5. ✅ SSL/TLS for secure connections
6. ✅ Gradio API enabled and accessible
7. ✅ Monitoring and maintenance procedures

Your application should now be accessible at:
- Web UI: `https://your-domain.com`
- API: `https://your-domain.com/api`
- API Docs: `https://your-domain.com/api/docs`

For support or questions, check the logs and troubleshooting section above.
