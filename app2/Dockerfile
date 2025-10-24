FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN groupadd -g 1000 nonroot_group
RUN useradd -u 1000 -g nonroot_group -s /bin/bash -m nonroot_user

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .. .

USER nonroot_user
