# HCI Project Deployment Guide

This guide explains how to deploy the HCI project on an Ubuntu dev server with Docker.

## Prerequisites

1. **Ubuntu Server** (20.04 or later)
2. **Docker** and **Docker Compose** installed
3. **Git** installed
4. **Domain name** (optional but recommended) or server IP address

## Initial Setup

### 1. Install Docker and Docker Compose

```bash
# Update package list
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker installation
docker --version
docker compose version
```

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/hci-project.git
cd hci-project
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp backend/.env.example backend/.env

# Edit the .env file with your actual values
nano backend/.env
```

**Important variables to set:**
- `SECRET_KEY`: Generate a secure random string
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Database credentials
- R2 credentials if using Cloudflare R2 storage

### 4. Build and Start Containers

```bash
# Build and start all containers
docker compose up -d

# Check container status
docker compose ps

# View logs
docker compose logs -f
```

## Project Structure

```
hci-project/
├── backend/
│   ├── Dockerfile          # Backend container configuration
│   ├── .env                # Environment variables (not in git)
│   ├── .env.example        # Example environment file
│   └── src/                # Application source code
├── nginx/
│   ├── nginx.conf          # Main nginx configuration
│   └── conf.d/
│       └── default.conf    # Site-specific configuration
├── docker-compose.yaml     # Multi-container orchestration
└── deploy.sh              # Deployment script
```

## Accessing Your Application

After deployment, your API will be accessible at:

- **Main API**: `http://YOUR_SERVER_IP/` or `http://your-domain.com/`
- **Health Check**: `http://YOUR_SERVER_IP/health`
- **API Documentation**: `http://YOUR_SERVER_IP/docs`
- **API Endpoints**: `http://YOUR_SERVER_IP/api/*`

### Port Configuration

- **Port 80**: HTTP traffic (nginx)
- **Port 443**: HTTPS traffic (nginx, requires SSL setup)
- **Port 5433**: PostgreSQL (exposed for debugging, can be removed in production)

## Deployment Script

Use the provided `deploy.sh` script to update your deployment:

```bash
# Make it executable (first time only)
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

The script will:
1. Pull latest changes from git
2. Stop running containers
3. Rebuild the backend image
4. Start all containers
5. Show deployment status

## Manual Deployment Steps

If you prefer manual control:

```bash
# Pull latest changes
git pull origin dev

# Rebuild and restart containers
docker compose down
docker compose build --no-cache backend
docker compose up -d

# Check status
docker compose ps
docker compose logs -f
```

## SSL/HTTPS Setup (Recommended for Production)

To enable HTTPS with Let's Encrypt:

1. **Install Certbot**:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain SSL Certificate**:
```bash
sudo certbot --nginx -d your-domain.com
```

3. **Update nginx configuration** to redirect HTTP to HTTPS

## Monitoring and Maintenance

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f nginx
docker compose logs -f db
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart backend
```

### Database Backup

```bash
# Backup database
docker exec postgres-db-hci pg_dump -U HCI HCIDB > backup_$(date +%Y%m%d).sql

# Restore database
docker exec -i postgres-db-hci psql -U HCI HCIDB < backup_20241201.sql
```

### Clean Up

```bash
# Remove stopped containers
docker compose down

# Remove all containers and volumes (⚠️ WARNING: This deletes all data)
docker compose down -v

# Clean up unused images
docker image prune -a
```

## Troubleshooting

### Containers won't start
```bash
# Check logs
docker compose logs

# Check if ports are already in use
sudo netstat -tulpn | grep -E ':(80|443|5433|8000)'
```

### Database connection issues
```bash
# Check if database is healthy
docker compose ps
docker compose exec db pg_isready -U HCI

# Check database logs
docker compose logs db
```

### Backend health check failing
```bash
# Check backend logs
docker compose logs backend

# Test health endpoint directly
docker compose exec backend curl http://localhost:8000/health
```

### Permission issues
```bash
# Fix ownership (run from project root)
sudo chown -R $USER:$USER .
```

## Security Recommendations

1. **Change default passwords** in `.env`
2. **Use strong SECRET_KEY** (generate with `openssl rand -hex 32`)
3. **Enable firewall**:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```
4. **Don't expose PostgreSQL port** in production (remove `ports` from db service)
5. **Set up SSL/HTTPS** with Let's Encrypt
6. **Regular backups** of database and volumes

## Auto-Deployment with Git Webhooks (Optional)

To automatically deploy when pushing to dev branch:

1. Create a webhook endpoint on your server
2. Configure GitHub webhook to call your endpoint
3. The endpoint script runs `./deploy.sh`

Example webhook handler (using webhook package):
```bash
sudo apt install webhook
# Configure webhook.json and set up systemd service
```

## Performance Optimization

- **Enable gzip compression** (already configured in nginx)
- **Set up CDN** for static assets
- **Database connection pooling** (configured in SQLAlchemy)
- **Monitor resource usage**: `docker stats`

## Support

For issues or questions:
- Check logs: `docker compose logs -f`
- Review GitHub issues
- Check FastAPI documentation: https://fastapi.tiangolo.com/