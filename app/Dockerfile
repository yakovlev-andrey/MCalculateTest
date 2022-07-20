FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip==22.1.2
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
