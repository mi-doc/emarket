FROM python:3.8.9-alpine3.13
LABEL maintainer='Mihail Nikolaev m.nikolaev1@gmail.com'

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /Emarket/requirements.txt
WORKDIR /Emarket
EXPOSE 8000

RUN apk update
# For Pillow
RUN apk add --update --no-cache tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev \
    libwebp-dev tcl-dev harfbuzz-dev
# For postgres
RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .build-deps build-base linux-headers py3-setuptools \
    python3-dev postgresql-dev musl-dev
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip
RUN /py/bin/pip install -r requirements.txt && \
    apk del .build-deps && \
    adduser --disabled-password --no-create-home app
COPY . /Emarket/

ENV PATH="/py/bin:$PATH"

USER app

