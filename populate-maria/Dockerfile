FROM python:3.8.3-alpine

RUN apk add -U --no-cache python3-dev py3-pip build-base

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

RUN rm -f requirements.txt

COPY ./populate-maria.py /app/

#WORKDIR /app

#RUN python3 populate-maria.py
