FROM python:3.8

RUN apt update && apt install sqlite python3-bs4 -f -y

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt
CMD [ "python", "-m", "bot" ]
