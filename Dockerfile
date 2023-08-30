# set base image
FROM python:3.8-slim 

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# defines the environment to development
ENV FLASK_ENV=development

# defines an env variable to be the directory of rooms
ENV ROOMS_FILES_PATH rooms/

# declare an env variable to be the file of users.csv
ENV CSV_PATH  data/users.csv

# tells Docker that a container listens for traffic on the specified port.
EXPOSE 5000

# copy the content of all the local directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "./chatApp.py" ]
