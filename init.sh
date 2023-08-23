#!/bin/bash
docker build -t project . 
docker run --name chatApp -d -p 5000:5000 project