FROM python:3.8.9-alpine3.13
LABEL maintainer='Mikhail Nikolaev'

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /Emarket/requirements.txt
WORKDIR /Emarket
EXPOSE 8000

RUN apk update && apk add --update --no-cache tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev \
        libwebp-dev tcl-dev harfbuzz-dev postgresql-client  && \
    apk add --update --no-cache --virtual .build-deps build-base linux-headers py3-setuptools \
        python3-dev postgresql-dev musl-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    apk del .build-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol

COPY ./scripts /scripts
RUN chmod -R +x /scripts
ENV PATH="/scripts:/py/bin:$PATH"

COPY . /Emarket/

# USER app
