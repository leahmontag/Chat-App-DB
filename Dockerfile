FROM python:3.8-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_ENV=development

ENV ROOMS_FILES_PATH rooms/

ENV CSV_PATH  data/users.csv

EXPOSE 5000

RUN apt-get update && apt-get install -y curl

HEALTHCHECK --interval=10s --timeout=3s \
CMD curl -fail http://localhost:5000/health || exit 1

COPY . .

CMD [ "python", "./chatApp.py" ]
