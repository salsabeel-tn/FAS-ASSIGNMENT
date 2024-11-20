#!/bin/bash

# Export required variables for docker-compose
export PYTHONPATH=$PYTHONPATH:/UPISAS
export GITHUB_REPOSITORY_URL=https://github.com/vidyawantstobattle/config-server
export GITHUB_OAUTH=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
export ARCH=arm64  # Change to 'amd64' if needed

# Start the Docker setup
echo "Starting the Docker setup with docker-compose..."
docker-compose up -d
echo "Docker containers started."
