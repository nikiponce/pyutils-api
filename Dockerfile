FROM python:3.8.10-slim

WORKDIR /app

COPY ./app /app

RUN pip install -r requirements.txt