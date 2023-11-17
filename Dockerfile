FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /code/src

WORKDIR /code

COPY requirements.txt ./

RUN pip install --upgrade pip==23.1.2 && \
    pip install --no-cache-dir -r ./requirements.txt

WORKDIR /code/src

COPY ./src /code/src
