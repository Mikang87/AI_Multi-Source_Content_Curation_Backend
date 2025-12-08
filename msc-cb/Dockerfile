FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev pkg-config gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app