#!/bin/bash

# Delete an img and it's according img by their names and img tag
image=$1
container=$2

if [ "" !=  "$container" ]; then
    docker rm -f $container
fi
if [ "" !=  "$image" ]; then
    docker image rm $image -f
fi


