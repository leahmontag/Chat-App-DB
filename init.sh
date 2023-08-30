# !/bin/bash
docker volume create chat-data
docker build -t chat_img:v0.0.0 .
docker run -v chat-data:/chatApp/data -d -p 5000:5000 --name chat_con --memory=1g --memory-reservation=512m --cpus=1 --cpuset-cpus=2 chat_img:v0.0.0




