#!/bin/bash
#docker rm -f storage-service
docker stop storage-service
docker system prune -f

