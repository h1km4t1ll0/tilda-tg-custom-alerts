# ---- Base python ----
FROM python:3.11 AS base
RUN apt-get update
RUN mkdir /app
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
RUN DEBIAN_FRONTEND=noninteractive apt install -y gcc python3-dev

# ---- Release ----
FROM dependencies AS build
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY ./ /app
