# 🚀 Deployment Checklist

## Pre-Deployment

### ✅ Development Complete
- [x] API endpoints implemented and tested
- [x] Web UI created and functional
- [x] Crawling works (30-50 pages)
- [x] Auto-indexing works
- [x] Q&A with source citations works
- [x] Refusal mechanism tuned
- [x] Error handling in place
- [x] Documentation complete

### ✅ Testing Complete
- [x] Tested with example.com (small site)
- [x] Tested with republicworld.com (medium site)
- [x] Evaluated with trap questions
- [x] Verified refusal mechanism
- [x] Performance tested (1-5ms queries)
- [x] UI tested in browser

---

## Deployment Options

### Option 1: Local Deployment (Current)

**Status:** ✅ Ready to use now

**Steps:**
```bash
# Windows
.\start.ps1

# Linux/Mac
./start.sh
```

**Access:**
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

**Best for:**
- Development
- Internal use
- Small teams
- Testing

---

### Option 2: Production Server

**Requirements:**
- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8+
- 2GB RAM minimum
- 10GB disk space

**Steps:**

1. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

2. **Clone/Upload Project**
```bash
# Upload your project files
scp -r rag-fastapi user@server:/opt/
```

3. **Setup Environment**
```bash
cd /opt/rag-fastapi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. **Run with Systemd** (recommended)
```bash
# Create service file
sudo nano /etc/systemd/system/rag-api.service
```

Content:
```ini
[Unit]
Description=RAG API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/rag-fastapi
Environment="PATH=/opt/rag-fastapi/.venv/bin"
ExecStart=/opt/rag-fastapi/.venv/bin/uvicorn app.api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable rag-api
sudo systemctl start rag-api
sudo systemctl status rag-api
```

5. **Setup Nginx** (optional, for HTTPS)
```bash
sudo apt install nginx

# Create config
sudo nano /etc/nginx/sites-available/rag-api
```

Content:
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

```bash
sudo ln -s /etc/nginx/sites-available/rag-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **Setup SSL** (recommended)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

**Best for:**
- Production use
- Multiple users
- External access
- 24/7 availability

---

### Option 3: Docker Deployment

**Requirements:**
- Docker installed
- Docker Compose (optional)

**Steps:**

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build Image**
```bash
docker build -t rag-api:latest .
```

3. **Run Container**
```bash
docker run -d \
  --name rag-api \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  rag-api:latest
```

4. **Or use Docker Compose**
```yaml
version: '3.8'

services:
  rag-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

```bash
docker-compose up -d
```

**Best for:**
- Cloud deployment
- Kubernetes
- Scalability
- Portability

---

### Option 4: Cloud Deployment

#### AWS EC2
1. Launch EC2 instance (t3.medium or larger)
2. Follow "Production Server" steps above
3. Configure security group (allow port 8000 or 80/443)
4. Use Elastic IP for stable address

#### Azure App Service
1. Create App Service (Python 3.11)
2. Deploy via GitHub Actions or Azure CLI
3. Configure startup command: `uvicorn app.api:app --host 0.0.0.0 --port 8000`

#### Google Cloud Run
1. Build Docker image
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Auto-scales based on traffic

#### Heroku
1. Create Procfile: `web: uvicorn app.api:app --host 0.0.0.0 --port $PORT`
2. Deploy via Git: `git push heroku main`

**Best for:**
- Managed infrastructure
- Auto-scaling
- Global reach
- High availability

---

## Post-Deployment

### ✅ Verification Checklist

- [ ] Server is running and accessible
- [ ] Web UI loads at root URL
- [ ] Health endpoint returns 200 OK
- [ ] API docs accessible at /docs
- [ ] Can crawl a test website
- [ ] Can ask questions and get answers
- [ ] Sources display correctly
- [ ] Performance is acceptable (<10ms queries)
- [ ] Error handling works
- [ ] Logs are being written

### ✅ Monitoring Setup

**Basic Monitoring:**
```bash
# Check server status
systemctl status rag-api

# View logs
journalctl -u rag-api -f

# Check resource usage
htop
```

**Advanced Monitoring:**
- Setup Prometheus + Grafana
- Add health check monitoring
- Setup alerting for downtime
- Monitor query latency
- Track error rates

### ✅ Security Hardening

- [ ] Enable HTTPS (SSL certificate)
- [ ] Configure firewall (only open necessary ports)
- [ ] Add rate limiting
- [ ] Enable CORS properly (not allow_origins=["*"])
- [ ] Setup authentication (if needed)
- [ ] Regular security updates
- [ ] Backup data directory

### ✅ Performance Optimization

- [ ] Enable gzip compression
- [ ] Add caching for static files
- [ ] Configure CDN for static assets
- [ ] Monitor and optimize query performance
- [ ] Setup load balancing (if high traffic)

---

## Maintenance

### Daily
- Check server health
- Monitor error logs
- Verify queries are working

### Weekly
- Review query performance
- Check disk space (data directory)
- Update dependencies if needed

### Monthly
- Full backup of data directory
- Security updates
- Performance review
- User feedback review

---

## Rollback Plan

If deployment fails:

1. **Stop new service**
```bash
sudo systemctl stop rag-api
```

2. **Restore previous version**
```bash
cd /opt/rag-fastapi
git checkout previous-version
systemctl restart rag-api
```

3. **Verify working**
```bash
curl http://localhost:8000/health
```

---

## Support

### Troubleshooting

**Service won't start:**
```bash
# Check logs
journalctl -u rag-api -n 50

# Check permissions
ls -la /opt/rag-fastapi

# Check port availability
netstat -tuln | grep 8000
```

**High memory usage:**
- Reduce max_pages in crawl
- Restart service periodically
- Monitor with htop

**Slow queries:**
- Check if index is built
- Verify chunk count
- Monitor CPU usage

---

## Current Status

**Environment:** Development/Local
**Status:** ✅ Ready for Production
**Next Step:** Choose deployment option above

**Quick Start Production:**
```bash
# Stop current dev server
Ctrl+C in terminal

# Start production mode
.\start.ps1  # Windows
./start.sh   # Linux/Mac

# Or deploy to server (see Option 2)
```

---

**Deployment is ready! Choose your option and go live.** 🚀
