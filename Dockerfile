FROM python:3.8-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_ENV=development

COPY . .

EXPOSE 5000

ENV ROOMS_FILES_PATH rooms/

CMD [ "python", "./chatApp.py" ]
