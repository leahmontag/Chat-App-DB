#!/bin/bash
read version commit_hash
img_name_and_tag="chat_img:${version}"
docker volume create chat-data
docker build -t  $img_name_and_tag .
git tag ${version} ${commit_hash} 
git push origin ${version}
