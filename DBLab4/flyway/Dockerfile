FROM flyway/flyway:latest-alpine

WORKDIR /usr/src/flyway

USER root

RUN apk update && \
    apk add --no-cache netcat-openbsd

COPY ./sql /flyway/sql
COPY ./conf /flyway/conf

ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_HOST
ARG POSTGRES_PORT

ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT

ENTRYPOINT ["sh", "-c", "nc -l -p 3000 -q 1 && \
    for i in $(seq 1 20); do \
    flyway migrate && break || { \
        echo 'Migration failed. Retrying in 2 seconds...'; \
        sleep 2; \
    } done && echo 'Migration successful!' && \
    echo 'Migration completed' | nc app 3000"]

