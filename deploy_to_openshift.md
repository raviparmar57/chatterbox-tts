# Quick OpenShift Deployment Guide

## Step-by-Step Commands

### Step 1: Login to OpenShift (Already Done ✓)
```bash
oc whoami
# Output: casabor968

oc project
# Output: Using project "casabor968-dev"
```

### Step 2: Delete Old Service and Route (Clean Start)
```bash
oc delete svc centos-gradio-svc
oc delete route centos-gradio-route
oc delete route centos-gradio-svc
```

### Step 3: Deploy New Application

**Option A: From GitHub (If you have pushed code)**
```bash
oc new-app python:3.11~https://github.com/YOUR-USERNAME/chatterbox-tts.git \
  --name=chatterbox-tts \
  --env GRADIO_SERVER_PORT=8080
```

**Option B: From Local Directory (Using Dockerfile)**
```bash
# First, create a new build config
oc new-build --name=chatterbox-tts --binary --strategy=docker

# Start the build with current directory
oc start-build chatterbox-tts --from-dir=. --follow

# Create the application from the built image
oc new-app chatterbox-tts

# Set environment variables
oc set env deployment/chatterbox-tts \
  GRADIO_SERVER_NAME=0.0.0.0 \
  GRADIO_SERVER_PORT=8080
```

### Step 4: Expose the Service (Create Public URL)
```bash
# Create route
oc expose svc/chatterbox-tts --port=8080

# Create secure HTTPS route (recommended)
oc create route edge chatterbox-tts-secure \
  --service=chatterbox-tts \
  --port=8080 \
  --insecure-policy=Redirect
```

### Step 5: Get Your Public URL
```bash
oc get routes
```

### Step 6: Check Status
```bash
# Check pods
oc get pods

# Check logs
oc logs -f deployment/chatterbox-tts

# Check service
oc get svc
```

### Step 7: Test API
```bash
# Get the route URL first
export ROUTE_URL=$(oc get route chatterbox-tts -o jsonpath='{.spec.host}')

# Test the endpoint
curl http://$ROUTE_URL
```

## Troubleshooting

### If pod is not starting:
```bash
# Check pod status
oc get pods

# Describe pod for details
oc describe pod <pod-name>

# View logs
oc logs <pod-name>
```

### If build fails:
```bash
# Check build logs
oc logs -f bc/chatterbox-tts

# Restart build
oc start-build chatterbox-tts --follow
```

### Scale resources if needed:
```bash
# Set resource limits
oc set resources deployment/chatterbox-tts \
  --limits=memory=4Gi,cpu=2 \
  --requests=memory=2Gi,cpu=500m
```
