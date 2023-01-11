# syntax=docker/dockerfile:1.4
FROM python:3.10 AS builder

WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]