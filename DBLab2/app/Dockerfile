FROM python:3.10.7-slim-buster

RUN mkdir -p /usr/src/temp
WORKDIR /usr/src/temp

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/temp/requirements.txt
RUN pip install -r requirements.txt

RUN apt update \
  && apt install -y curl \
  && apt install -y p7zip-full \
  && apt-get install -y postgresql-client-11

ENV DB_DATA_YEAR1=2020
ENV DB_DATA_YEAR2=2019

# how many inserts of each table
ENV DB_DATA_LIMIT=10000

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


RUN 7z x OpenDataZNO${DB_DATA_YEAR1}.7z
RUN 7z x OpenDataZNO${DB_DATA_YEAR2}.7z

COPY . /usr/src/temp/

CMD ["python", "main.py"]
