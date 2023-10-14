FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_ENV=development

ENV ROOMS_FILES_PATH rooms/

ENV CSV_PATH  data/users.csv

EXPOSE 5000

COPY . .

CMD [ "python", "./chatApp.py" ]
