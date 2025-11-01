FROM python:3.12-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache ffmpeg tesseract-ocr tesseract-ocr-data-rus tesseract-ocr-data-ukr tesseract-ocr-data-deu build-base libxml2-dev libxslt-dev cargo

WORKDIR /app

COPY . /app/

RUN addgroup -g 2000 app && adduser -u 2000 -G app -s /bin/sh -D app && chown -R 2000:2000 /app
USER 2000

RUN mkdir db

RUN pip install uv
RUN python -m uv sync

ENV TZ="Europe/Moscow"

ENTRYPOINT ["python", "-m", "uv", "run", "python", "-m", "bot"]
