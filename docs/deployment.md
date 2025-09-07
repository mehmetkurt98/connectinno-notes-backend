# Deployment Documentation

## Overview

This document provides detailed instructions for deploying the Connectinno Notes Backend API to various platforms.

## Deployment Options

### 1. Local Development

#### Prerequisites
- Python 3.8+
- Virtual environment
- Firebase project setup
- Google Gemini API key

#### Steps
```bash
# Clone repository
git clone <repository-url>
cd connectinno_backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp env.example .env
# Edit .env with your values

# Run application
uvicorn main:app --reload --port 8000
```

### 2. Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - FIREBASE_SERVICE_ACCOUNT_PATH=/app/serviceAccountKey.json
    volumes:
      - ./serviceAccountKey.json:/app/serviceAccountKey.json:ro
    restart: unless-stopped
```

#### Build and Run
```bash
# Build image
docker build -t connectinno-backend .

# Run container
docker run -p 8000:8000 \
  -e FIREBASE_PROJECT_ID=your-project-id \
  -e GEMINI_API_KEY=your-api-key \
  -v $(pwd)/serviceAccountKey.json:/app/serviceAccountKey.json:ro \
  connectinno-backend

# Or use docker-compose
docker-compose up -d
```

### 3. Cloud Deployment

#### Heroku

1. **Create Heroku App**
```bash
heroku create connectinno-backend
```

2. **Set Environment Variables**
```bash
heroku config:set FIREBASE_PROJECT_ID=your-project-id
heroku config:set GEMINI_API_KEY=your-api-key
```

3. **Deploy**
```bash
git push heroku main
```

#### Railway

1. **Connect Repository**
   - Go to Railway dashboard
   - Connect your GitHub repository
   - Select the backend folder

2. **Set Environment Variables**
   - Add all required environment variables
   - Upload service account key

3. **Deploy**
   - Railway automatically deploys on push

#### AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - Configure security groups (port 8000)

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

3. **Deploy Application**
```bash
git clone <repository-url>
cd connectinno_backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Run with Systemd**
```ini
[Unit]
Description=Connectinno Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/connectinno_backend
Environment=PATH=/home/ubuntu/connectinno_backend/.venv/bin
ExecStart=/home/ubuntu/connectinno_backend/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## Environment Variables

### Required Variables
```env
FIREBASE_PROJECT_ID=your-firebase-project-id
GEMINI_API_KEY=your-gemini-api-key
FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
```

### Optional Variables
```env
HOST=0.0.0.0
PORT=8000
DEBUG=false
CORS_ORIGINS=["https://yourdomain.com"]
LOG_LEVEL=info
```

## Security Considerations

### 1. Environment Variables
- Never commit `.env` files
- Use secure secret management
- Rotate API keys regularly

### 2. Firebase Service Account
- Keep service account key secure
- Use least privilege principle
- Monitor access logs

### 3. CORS Configuration
- Restrict CORS origins in production
- Use HTTPS only
- Validate all inputs

### 4. Rate Limiting
- Implement rate limiting
- Use reverse proxy (Nginx)
- Monitor for abuse

## Monitoring and Logging

### 1. Application Logs
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. Health Checks
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

### 3. Metrics
- Response times
- Error rates
- Request counts
- Resource usage

## Performance Optimization

### 1. Database Connection Pooling
```python
# Configure Firestore connection pooling
db = firestore.Client()
```

### 2. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_data(key: str):
    # Cache frequently accessed data
    pass
```

### 3. Async Operations
```python
import asyncio

async def process_requests():
    # Use async for I/O operations
    pass
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### 2. Firebase Authentication Errors
- Check service account key
- Verify project ID
- Ensure Firestore is enabled

#### 3. Gemini API Errors
- Verify API key
- Check rate limits
- Monitor quota usage

#### 4. CORS Issues
- Check CORS configuration
- Verify allowed origins
- Test with different browsers

## Backup and Recovery

### 1. Database Backup
```bash
# Export Firestore data
gcloud firestore export gs://your-bucket/backup
```

### 2. Application Backup
```bash
# Backup application code
tar -czf backup.tar.gz connectinno_backend/
```

### 3. Configuration Backup
```bash
# Backup environment variables
heroku config > config-backup.txt
```

## Scaling Considerations

### 1. Horizontal Scaling
- Use load balancer
- Deploy multiple instances
- Implement session management

### 2. Database Scaling
- Use Firestore auto-scaling
- Implement caching layer
- Optimize queries

### 3. API Rate Limiting
- Implement rate limiting
- Use Redis for distributed rate limiting
- Monitor and adjust limits

## Maintenance

### 1. Regular Updates
- Update dependencies
- Security patches
- Performance improvements

### 2. Monitoring
- Set up alerts
- Monitor logs
- Track performance metrics

### 3. Backup Strategy
- Regular database backups
- Configuration backups
- Disaster recovery plan
