# #!/bin/bash
# set -e

# version="$1"
# git_version="v${version}"
# commit_hash="$2"

# if [ -z "$version" ]; then
#     echo "Error: Missing parameter. Please run the script again with the desired version."
#     exit 1
# fi

# img_name_and_tag="chat_img:${version}"

# #----------------------------------------------------------------------------
# # building the img
# #----------------------------------------------------------------------------

# # Check if the image already exists & discarding the output
# if docker image inspect "$img_name_and_tag" >/dev/null 2>&1; then
#     echo "The image already exists."
#     read -p "Do you want to rebuild the image? (y/n): " rebuild_choice

#     if [ "$rebuild_choice" = "y" ] || [ "$rebuild_choice" = "Y" ]; then
#         echo "Deleting existing image..."
#         docker image rm "$img_name_and_tag"
#     else
#         echo "Using the existing image."
#         exit 0
#     fi
# fi

# docker volume create chat-data
# docker build -t "$img_name_and_tag" . 

# #----------------------------------------------------------------------------
# # Updating the repo
# #----------------------------------------------------------------------------

# # Check if commit hash is provided 
# if [ -n "$commit_hash" ]; then
#     git tag "$version" "$commit_hash"
#     git push origin "$version"
# else
#     echo "Commit hash not provided. Skipping tagging and pushing to the repository."
# fi














#!/bin/bash
set -e

version="$1"
git_version="v${version}"
commit_hash="$2"

if [ -z "$version" ]; then
    echo "Error: Missing parameter. Please run the script again with the desired version."
    exit 1
fi

img_name_and_tag="chat_img:${version}"

#----------------------------------------------------------------------------
# building the img
#----------------------------------------------------------------------------

# Check if the image already exists & discarding the output
if docker image inspect "$img_name_and_tag" >/dev/null 2>&1; then
    echo "The image already exists."
    read -p "Do you want to rebuild the image? (y/n): " rebuild_choice

    if [ "$rebuild_choice" = "y" ] || [ "$rebuild_choice" = "Y" ]; then
        echo "Deleting existing image..."
        docker image rm "$img_name_and_tag"
    else
        echo "Using the existing image."
        exit 0
    fi
fi

docker volume create chat-data
docker build -t "$img_name_and_tag" . 

#----------------------------------------------------------------------------
# Updating the repo
#----------------------------------------------------------------------------

# Check if commit hash is provided 
if [ -n "$commit_hash" ]; then
    git tag "$version" "$commit_hash"
    git push origin "$version"
    echo "successfully pushed" 
else
    echo "Commit hash not provided. Skipping tagging and pushing to the repository."
fi

# gcloud config set auth/impersonate_service_account artifact-admin-sa@grunitech-mid-project.iam.gserviceaccount.com
# gcloud auth configure-docker me-west1-docker.pkg.dev

# me-west1-docker.pkg.dev/grunitech-mid-project/ chanafeiga-chat-app-images/first-try
# Project id = grunitech-mid-project

