FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    python2-dev gpgme-dev libc-dev \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
    python3-dev libffi-dev openssl-dev cargo
RUN pip install --upgrade pip
RUN pip uninstall PIL
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /server
WORKDIR /server
COPY ./server /server

RUN python manage.py collectstatic --noinput