# Set base image
FROM python:alpine

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Define the environment to development
ENV FLASK_ENV=development

# Define an environment variable for the directory of rooms
ENV ROOMS_FILES_PATH rooms/

# Declare an environment variable for the users.csv file
ENV CSV_PATH data/users.csv

# Expose port 5000
EXPOSE 5000

# Install curl
RUN apk --no-cache add curl

# HEALTHCHECK
HEALTHCHECK --interval=10s --timeout=3s CMD curl -fail http://localhost:5000/health || exit 1

# Copy the content of the local directory to the working directory
COPY . .

# Command to run on container start
CMD ["python", "./chatApp.py"]
