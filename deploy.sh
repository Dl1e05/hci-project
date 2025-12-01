#!/bin/bash

# HCI Project Deployment Script
# This script pulls the latest changes from git and rebuilds/restarts the Docker containers

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  HCI Project Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}Warning: Running as root. Consider using a non-root user with docker group membership.${NC}"
fi

# Function to print step
print_step() {
    echo -e "\n${GREEN}==>${NC} $1"
}

# Function to print error
print_error() {
    echo -e "\n${RED}ERROR:${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Determine docker compose command
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    print_error "backend/.env file not found. Please create it from backend/.env.example"
    exit 1
fi

# Pull latest changes from git
print_step "Pulling latest changes from git..."
if [ -d ".git" ]; then
    git fetch origin
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo "Current branch: $CURRENT_BRANCH"

    # Stash any local changes
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}Local changes detected. Stashing...${NC}"
        git stash
    fi

    git pull origin "$CURRENT_BRANCH"
    echo -e "${GREEN}Git pull completed${NC}"
else
    echo -e "${YELLOW}Not a git repository. Skipping git pull.${NC}"
fi

# Stop running containers
print_step "Stopping running containers..."
$DOCKER_COMPOSE down

# Remove old images (optional - uncomment if you want to clean up)
# print_step "Removing old images..."
# docker image prune -f

# Build new images
print_step "Building Docker images..."
$DOCKER_COMPOSE build --no-cache frontend backend

# Start containers
print_step "Starting containers..."
$DOCKER_COMPOSE up -d

# Wait for services to be healthy
print_step "Waiting for services to be healthy..."
sleep 5

# Check container status
print_step "Checking container status..."
$DOCKER_COMPOSE ps

# Show logs
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To view logs, run:"
echo "  $DOCKER_COMPOSE logs -f"
echo ""
echo "To check service status:"
echo "  $DOCKER_COMPOSE ps"
echo ""
echo "Your application should be accessible at:"
echo "  - http://YOUR_SERVER_IP/ (Frontend - Next.js)"
echo "  - http://YOUR_SERVER_IP/api/* (Backend API endpoints)"
echo "  - http://YOUR_SERVER_IP/api/health (API health check)"
echo "  - http://YOUR_SERVER_IP/api/docs (API documentation)"
echo ""