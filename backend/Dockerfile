FROM java:latest
COPY ./seeds /opt/seeds
ENTRYPOINT ["/bin/bash", "/opt/seeds/start_seeds.sh"]
EXPOSE 9999/tcp
