#!/bin/bash

# Stop and remove all containers, networks, and volumes created by Docker Compose
docker compose -f docker/docker-compose.yml down --volumes --remove-orphans

# Remove all images related to the project
docker images --filter "label=com.docker.compose.project=$(basename $(pwd))" -q | xargs docker rmi -f

# Remove all volumes related to the project
docker volume ls --filter "label=com.docker.compose.project=$(basename $(pwd))" -q | xargs docker volume rm

# Remove all networks related to the project
docker network ls --filter "label=com.docker.compose.project=$(basename $(pwd))" -q | xargs docker network rm

# Rebuild the Docker images without using the cache
docker compose -f docker/docker-compose.yml build --no-cache

# Start the containers
docker compose -f docker/docker-compose.yml up
