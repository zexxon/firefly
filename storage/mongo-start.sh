#!/bin/bash
docker run --name storage-service -p=27017:27017 -v /data/1:/data/db -v /data/2:/data/configdb -d storage:latest
#docker attach storage-service 
