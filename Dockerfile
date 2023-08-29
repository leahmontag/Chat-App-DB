FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_ENV=development

COPY . .

EXPOSE 5000

ENV ROOMS_FILES_PATH rooms/

ENV CSV_PATH  data/users.csv

CMD [ "python", "./chatApp.py" ]
