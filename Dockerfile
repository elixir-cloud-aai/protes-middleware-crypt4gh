# Dockerfile for athitheyag/c4gh:1.0
FROM python:3.12

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt