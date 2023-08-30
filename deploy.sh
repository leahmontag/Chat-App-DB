#!/bin/bash

#Stop the Execution on the First Error 
set -e  

version=$1
commit_hash=$2
if [ "" -eq $version] || ["" -eq $commit_hash ]; then
    echo "Error: Missing parameters, Try run again with the version did you want and the commit hash"
    exit 1
fi
img_name_and_tag="chat_img:v${version}"
docker volume create chat-data
docker build -t  $img_name_and_tag .
git tag ${version} ${commit_hash} 
git push origin ${version}
