FROM python:3.7-alpine

RUN apk update && apk --no-cache add make bash gettext postgresql-dev gcc python3-dev musl-dev linux-headers jpeg-dev zlib-dev ncurses-dev

WORKDIR /tmp
COPY ./requirements .
RUN pip install --upgrade pip
RUN pip install -r ./dev.txt

WORKDIR /app/server
