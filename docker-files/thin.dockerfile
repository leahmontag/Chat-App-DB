FROM python:3.8-slim AS reduce_docker_image

COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.8-slim

WORKDIR /code

COPY --from=reduce_docker_image /root/.local /root/.local

COPY . .

ENV FLASK_ENV=development

ENV ROOMS_FILES_PATH rooms/

ENV CSV_PATH  data/users.csv

ENV PATH=/root/.local:$PATH

EXPOSE 5000

CMD [ "python", "./chatApp.py" ]
