FROM python:3.8-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV ROOM_FILES_PATH /app/room_files

RUN mkdir room_files

CMD [ "python", "./chatApp.py" ]