#!/bin/bash
docker run --name backend-service -p=9999:9999 --net bridge --link cache-service --link storage-service -i -d backend-service:latest
docker attach backend-service
