
#!/bin/bash
script_folder='scripts'
OPTIONS="init delete exec deploy prune info"


if [ $# -eq 0 ]; then
echo "./automation.sh <-i|-d|-e|-de|-p|-in> <arguments>"
echo "Options:"
echo "  -i, --init   <Version> Build chat-app image with the version provided and run the chat-app container with mounted volumes"
echo "  -d, --delete <Version> Delete chat-app container and the specified chat-app image"
echo "  -e, --exec             Open a bash shell as root inside the chat-app container"
echo "  -de,--deploy <version> <commit-hash>"
echo "                         Build, tag, and push the chat-app image with the specified tag to GCR and [OPTIONAL]tag and push the commit hash"
echo "  -p, --prune            Prune all Docker resources"
echo "  -in, --info            Show all Docker resources"
exit 1
fi




#!/bin/bash


# Function to display usage information
display_usage() {
echo "./auto.sh <-i|-d|-e|-de|-p|-in> <arguments>"
echo "Options:"
echo "  -i, --init   <Version> Build chat-app image with the version provided and run the chat-app container with mounted volumes"
echo "  -d, --delete <Version> Delete chat-app container and the specified chat-app image"
echo "  -e, --exec             Open a bash shell as root inside the chat-app container"
echo "  -de,--deploy <version> <commit-hash>"
echo "                         Build, tag, and push the chat-app image with the specified tag to GCR and [OPTIONAL]tag and push the commit hash"
echo "  -p, --prune            Prune all Docker resources"
echo "  -in, --info            Show all Docker resources"
exit 1
}


# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    display_usage
fi


# Parse command-line options
while [ $# -gt 0 ]; do
    case "$1" in (-i|--init)
            if [ -n "$2" ]; then
                echo "Running init.sh with version $2"
                ./${script_folder}/init.sh "$2"
                shift 2
            else
                echo "Error: Version argument is missing for -i option."
                display_usage
            fi
            ;;
        -d|--delete)
            if [ -n "$2" ]; then
                echo "Running delete.sh with version $2"
                ./${script_folder}/delete.sh "$2"
                # shift 2
            else
                echo "Error: Version argument is missing for -d option."
                display_usage
            fi
            ;;
        -c|--cleanup)
                    echo "Running cleanup.sh "
                    ./${script_folder}/cleanup.sh 
                else
                    echo "Error: Version argument is missing for -d option."
                    display_usage
                fi
        ;;
        -e|--exec)
            echo "Opening a bash shell as root inside the chat-app container"
            # Add your command to open a bash shell here
            docker exec -it chat-app-run bash
            shift
            ;;
        -de|--deploy)
            if [ -n "$2" ] && [ -n "$3" ]; then
                echo "Building, tagging, and pushing chat-app image with tag $2 to GCR."
                echo "Optional: Tag and push commit hash $3"
                ./${script_folder}/deploy.sh $2 $3
                shift 3
            else
                echo "Error: Missing arguments for -de option."
                display_usage
            fi
            ;;
        -p|--prune)
            echo "Running prune.sh"
            ./${script_folder}/prune.sh
            shift
            ;;
        -in|--info)
            echo "Running info.sh"
            ./${script_folder}/info.sh
            shift
            ;;
        *)
            echo "Error: Unknown option $1"
            display_usage
            ;;
    esac
done
