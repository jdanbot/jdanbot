FROM python:3.11-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add ffmpeg --no-cache 
RUN apk add tesseract-ocr tesseract-ocr-data-* --no-cache 
RUN apk add gcc python3-dev musl-dev linux-headers --no-cache

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app/
RUN addgroup -g 2000 app && adduser -u 2000 -G app -s /bin/sh -D app && chown -R 2000:2000 /app
USER 2000

RUN poetry config virtualenvs.in-project true
RUN poetry lock --no-update
RUN poetry install

ENV TZ="Europe/Moscow"

CMD ["poetry", "run", "python", "-m", "bot"]