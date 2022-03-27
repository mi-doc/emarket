FROM python:3.8.9
LABEL maintainer='Mihail Nikolaev m.nikolaev1@gmail.com'

ENV PYTHONUNBUFFERED 1

COPY . /Emarket/
WORKDIR /Emarket
EXPOSE 8000

#RUN apk update && apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers libjpeg libjpeg python3-dev \
#    postgresql-dev musl-dev jpeg-dev zlib-dev
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip
RUN /py/bin/pip install -r requirements.txt && \
#    apk del .tmp && \
    adduser --disabled-password --no-create-home app

ENV PATH="/py/bin:$PATH"

USER app

