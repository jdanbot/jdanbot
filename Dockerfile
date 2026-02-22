FROM python:3.14.3-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache ffmpeg tesseract-ocr tesseract-ocr-data-rus tesseract-ocr-data-ukr tesseract-ocr-data-deu tesseract-ocr-data-eng git uv

WORKDIR /app

COPY . /app/

RUN addgroup -g 2000 app && adduser -u 2000 -G app -s /bin/sh -D app && chown -R 2000:2000 /app
USER 2000

RUN mkdir db

RUN uv sync

ENV TZ="Europe/Moscow"

ENTRYPOINT ["uv", "run", "python", "-m", "bot"]
