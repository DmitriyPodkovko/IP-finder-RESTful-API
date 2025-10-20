#!/bin/bash
set -e

echo "🛑 Stopping and removing all containers..."
if [ "$(docker ps -q)" ]; then
  docker stop $(docker ps -q)
  docker rm $(docker ps -aq)
else
  echo "No containers found."
fi

echo "🧹 Removing all volumes..."
volumes=$(docker volume ls -q)
if [ -n "$volumes" ]; then
  docker volume rm $volumes
else
  echo "No volumes found."
fi

echo "🧱 Removing all images..."
images=$(docker images -q)
if [ -n "$images" ]; then
  docker rmi -f $images
else
  echo "No images found."
fi

echo "🧽 Pruning unused volumes..."
docker volume prune -f

echo "🚀 Rebuilding containers..."
docker compose up --build -d --remove-orphans --force-recreate
