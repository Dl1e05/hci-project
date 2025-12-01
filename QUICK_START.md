# Quick Start Guide

## First Time Setup

1. **Copy environment file**:
   ```bash
   cp backend/.env.example backend/.env
   nano backend/.env  # Edit with your values
   ```

2. **Start containers**:
   ```bash
   docker compose up -d
   ```

3. **Check status**:
   ```bash
   docker compose ps
   docker compose logs -f
   ```

## Access Your Application

- **Frontend (Next.js)**: `http://YOUR_SERVER_IP/`
- **Backend API**: `http://YOUR_SERVER_IP/api/*`
- **API Docs**: `http://YOUR_SERVER_IP/api/docs`
- **Health Check**: `http://YOUR_SERVER_IP/api/health`

## Architecture

```
Internet → Nginx (Port 80)
            ├─→ Frontend (Next.js on port 3000) - All routes except /api/*
            └─→ Backend (FastAPI on port 8000) - /api/* routes
                └─→ Database (PostgreSQL on port 5432)
```

## Update Deployment

```bash
./deploy.sh
```

Or manually:
```bash
git pull origin dev
docker compose down
docker compose build --no-cache frontend backend
docker compose up -d
```

## Common Commands

```bash
# View logs (all services)
docker compose logs -f

# View specific service logs
docker compose logs -f frontend
docker compose logs -f backend
docker compose logs -f nginx

# Restart all services
docker compose restart

# Restart specific service
docker compose restart frontend

# Stop all services
docker compose down

# Rebuild
docker compose build --no-cache
```

## Need Help?

See detailed instructions in `DEPLOYMENT.md`