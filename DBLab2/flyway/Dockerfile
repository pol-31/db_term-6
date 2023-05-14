FROM flyway/flyway:latest-alpine

WORKDIR /usr/src/flyway

USER root

RUN apk update && \
    apk add --no-cache netcat-openbsd

COPY ./sql /flyway/sql
COPY ./conf /flyway/conf

ENTRYPOINT ["sh", "-c", "nc -l -p 3000 -q 1 && \
    for i in $(seq 1 20); do \
    flyway migrate && break || { \
        echo 'Migration failed. Retrying in 2 seconds...'; \
        sleep 2; \
    } done"]

