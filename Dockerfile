# Base image with Python 3.9 and dependencies
FROM python:3.9-slim-buster AS base

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home smartfert \
    && chown -R smartfert /home/smartfert
WORKDIR /home/smartfert

USER smartfert

ENV PATH="/home/smartfert/.local/bin:$PATH"

COPY --chown=smartfert requirements.txt .

WORKDIR /smartfert

COPY --chown=smartfert . .


EXPOSE 3000

RUN pip install --no-cache-dir -r requirements.txt

