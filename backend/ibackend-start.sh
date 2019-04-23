#!/bin/bash
docker run --name backend-service --link cache-service --link storage-service -i backend-service:latest
