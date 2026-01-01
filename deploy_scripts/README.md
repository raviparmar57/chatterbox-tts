# Deployment Scripts for CentOS VPS

This directory contains automated scripts to help you deploy Chatterbox TTS on a CentOS/RHEL VPS.

## Scripts Overview

1. **setup_vps.sh** - Initial VPS setup (system packages, Python, dependencies)
2. **install_app.sh** - Install the application and Python packages
3. **setup_service.sh** - Create and enable systemd service
4. **setup_nginx.sh** - Configure Nginx reverse proxy
5. **test_api.py** - Test the deployed API

## Quick Start Guide

### Step 1: Initial VPS Setup

SSH into your VPS and run:

```bash
chmod +x deploy_scripts/*.sh
./deploy_scripts/setup_vps.sh
```

### Step 2: Upload Application Files

From your local machine:

```bash
rsync -avz --progress ./ username@your-vps-ip:/opt/chatterbox-tts/
```

### Step 3: Install Application

On the VPS:

```bash
cd /opt/chatterbox-tts
./deploy_scripts/install_app.sh
```

### Step 4: Setup Service

```bash
./deploy_scripts/setup_service.sh
sudo systemctl start chatterbox-tts
sudo systemctl status chatterbox-tts
```

### Step 5: Configure Nginx (Optional)

```bash
./deploy_scripts/setup_nginx.sh
```

### Step 6: Test API

```bash
cd /opt/chatterbox-tts
source venv/bin/activate
python deploy_scripts/test_api.py http://localhost:7860
```

## Manual Deployment

If you prefer manual deployment, follow the comprehensive guide in `DEPLOYMENT_GUIDE.md`.

## Troubleshooting

See the troubleshooting section in `DEPLOYMENT_GUIDE.md`.
