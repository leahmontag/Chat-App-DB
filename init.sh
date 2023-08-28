#!/bin/bash
docker volume create chat-data
docker build -t chat_img . 
# docker run --name chat_con -d -p 5000:5000 chat_img
docker run -v chat-data:/chatApp/data -p 5000:5000 --name chat_con chat_img