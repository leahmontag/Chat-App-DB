# !/bin/bash
version=$1
if [ "" =  "$version" ]; then
    echo "Error: Missing parameter, Run again with the version did you want."
    exit 1
fi
docker volume create chat-data
docker build -t chat_img:${version} .
docker run -v chat-data:/chatApp/data -d -p 5000:5000 --name chat_con --memory=1g --memory-reservation=512m --cpus=1 --cpuset-cpus=2 chat_img:${version}

# cmd interval curl  - for route health 


