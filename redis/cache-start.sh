#!/bin/bash
docker run --name cache-service -d -v /opt/firefly/redis/data:/data cache:latest
#docker attach cache-service
