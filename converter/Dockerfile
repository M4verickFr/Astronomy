# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine AS builder

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]