FROM python:3.10.7-slim-buster

RUN mkdir -p /usr/src/results
RUN mkdir -p /usr/src/backups

WORKDIR /usr/src/app

USER root

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN apt update \
  && apt install -y curl \
  && apt install -y p7zip-full \
  && apt-get install -y postgresql-client-11


ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_HOST
ARG POSTGRES_PORT

ARG MONGO_INITDB_ROOT_USERNAME
ARG MONGO_INITDB_ROOT_PASSWORD
ARG MONGO_INITDB_DATABASE
ARG MONGO_HOSTNAME
ARG MONGO_PORT

ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT

ENV MONGO_INITDB_ROOT_USERNAME=$MONGO_INITDB_ROOT_USERNAME
ENV MONGO_INITDB_ROOT_PASSWORD=$MONGO_INITDB_ROOT_PASSWORD
ENV MONGO_INITDB_DATABASE=$MONGO_INITDB_DATABASE
ENV MONGO_HOSTNAME=$MONGO_HOSTNAME
ENV MONGO_PORT=$MONGO_PORT
            

ENV DB_DATA_YEAR1=2020
ENV DB_DATA_YEAR2=2019

# how many inserts of each table (or -1)
ENV DB_DATA_LIMIT=1000

# create main table (tbl_zno_results) or not (True or False)
ENV DB_DO_INIT=True

ARG URL1=https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO${DB_DATA_YEAR1}.7z 
ARG URL2=https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO${DB_DATA_YEAR2}.7z
ARG RETRIES=5
ARG RETRIES_COOLDOWN=2


# trying to download file 1

RUN for i in $(seq 1 ${RETRIES}); do curl --fail -O ${URL1};\
    if [ $? -eq 0 ]; then \
        echo "Download successful"; \
        break; \
    else \
        echo "Download failed. Retrying in ${RETRIES_COOLDOWN} seconds..."; \
        sleep ${RETRIES_COOLDOWN}; \
    fi; done


# trying to download file 2

RUN for i in $(seq 1 ${RETRIES}); do curl --fail -O ${URL2};\
    if [ $? -eq 0 ]; then \
        echo "Download successful"; \
        break; \
    else \
        echo "Download failed. Retrying in ${RETRIES_COOLDOWN} seconds..."; \
        sleep ${RETRIES_COOLDOWN}; \
    fi; done


RUN 7z x OpenDataZNO${DB_DATA_YEAR1}.7z -sdel
RUN 7z x OpenDataZNO${DB_DATA_YEAR2}.7z -sdel

COPY . /usr/src/app/

EXPOSE 5000

CMD ["python", "main.py"]
