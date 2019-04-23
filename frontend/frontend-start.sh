#!/bin/bash
docker run --name frontend-service -p=10000:10000 --link backend-service frontend-service -i -d frontend-service:latest
docker attach frontend-service 
