FROM python:3.11-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache ffmpeg tesseract-ocr $(apk search -q "tesseract-ocr-data-*") build-base linux-headers git
RUN apk add tesseract-ocr-data-afr tesseract-ocr-data-ara tesseract-ocr-data-aze tesseract-ocr-data-bel tesseract-ocr-data-ben tesseract-ocr-data-bul tesseract-ocr-data-cat tesseract-ocr-data-chr tesseract-ocr-data-dan tesseract-ocr-data-deu tesseract-ocr-data-enm tesseract-ocr-data-epo tesseract-ocr-data-equ tesseract-ocr-data-est tesseract-ocr-data-eus tesseract-ocr-data-fin tesseract-ocr-data-fra tesseract-ocr-data-frk tesseract-ocr-data-frm tesseract-ocr-data-glg tesseract-ocr-data-grc tesseract-ocr-data-heb tesseract-ocr-data-hin tesseract-ocr-data-hrv tesseract-ocr-data-hun tesseract-ocr-data-ind tesseract-ocr-data-isl tesseract-ocr-data-ita tesseract-ocr-data-jpn tesseract-ocr-data-kan tesseract-ocr-data-kat tesseract-ocr-data-kor tesseract-ocr-data-lav tesseract-ocr-data-lit tesseract-ocr-data-mal tesseract-ocr-data-mkd tesseract-ocr-data-mlt tesseract-ocr-data-msa tesseract-ocr-data-nld tesseract-ocr-data-nor tesseract-ocr-data-pol tesseract-ocr-data-por tesseract-ocr-data-ron tesseract-ocr-data-rus tesseract-ocr-data-slk tesseract-ocr-data-slv tesseract-ocr-data-spa tesseract-ocr-data-sqi tesseract-ocr-data-srp tesseract-ocr-data-swa tesseract-ocr-data-swe tesseract-ocr-data-tam tesseract-ocr-data-tel tesseract-ocr-data-tgl tesseract-ocr-data-tha tesseract-ocr-data-tur tesseract-ocr-data-ukr tesseract-ocr-data-vie

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

RUN addgroup -g 2000 app && adduser -u 2000 -G app -s /bin/sh -D app && chown -R 2000:2000 /app
USER 2000

RUN mkdir db

RUN poetry config virtualenvs.in-project true \
    && poetry lock \
	&& poetry install

ENV TZ="Europe/Moscow"

ENTRYPOINT ["poetry", "run", "python", "-m", "bot"]
