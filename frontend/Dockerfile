FROM node:9
WORKDIR /opt/firefly/frontend 
COPY ./frontend/package*.json ./
RUN npm install 
#RUN apt update
#RUN apt install net-tools
COPY ./frontend .
ENTRYPOINT ["/bin/bash", "/opt/firefly/frontend/frontend-start.sh"]
EXPOSE 10000

