#!/bin/bash
docker build -t chat_img . 
docker run --name chat_con -d -p 5000:5000 chat_img