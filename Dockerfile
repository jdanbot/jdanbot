FROM python:3.12-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache ffmpeg tesseract-ocr tesseract-ocr-data-rus tesseract-ocr-data-ukr tesseract-ocr-data-deu

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

RUN addgroup -g 2000 app && adduser -u 2000 -G app -s /bin/sh -D app && chown -R 2000:2000 /app
USER 2000

RUN poetry config virtualenvs.in-project true \
    && poetry lock --no-update \
	&& poetry install

ENV TZ="Europe/Moscow"

ENTRYPOINT ["poetry", "run", "python", "-m", "bot"]
