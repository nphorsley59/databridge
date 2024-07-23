#!/bin/bash

# Bring up the Docker containers defined in docker-compose.yml
docker compose -f docker/docker-compose.yml up -d --remove-orphans
