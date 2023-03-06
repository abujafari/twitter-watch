# pull official python alpine image
FROM python:3.11-alpine as base

# Set Environment Variable
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# Making source and static directory
RUN mkdir /src
RUN mkdir /static

# Creating Work Directory
WORKDIR /src

# Adding mandatory packages to docker
RUN apk update && apk add --no-cache postgresql zlib jpeg openblas libstdc++

# Installing temporary packages required for installing requirements.pip
RUN apk add --no-cache --virtual build-deps gcc python3-dev musl-dev postgresql-dev zlib-dev  jpeg-dev  g++ openblas-dev cmake \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h

# Update pip
RUN pip install --upgrade pip


FROM base as builder

# Installing requirements.pip from project
COPY ./requirements.txt /scripts/
RUN pip install --no-cache-dir -r /scripts/requirements.txt

# removing temporary packages from docker and removing cache
RUN apk del build-deps && \
    find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip
