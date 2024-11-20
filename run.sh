#!/bin/bash

# Export required variables for docker-compose
export PYTHONPATH=$PYTHONPATH:/UPISAS
# export GITHUB_REPOSITORY_URL=""
# export GITHUB_OAUTH=""
export ARCH=arm64  # Change to 'amd64' if needed

# Start the Docker setup
echo "Starting the Docker setup with docker-compose..."
docker-compose up -d
echo "Docker containers started."
