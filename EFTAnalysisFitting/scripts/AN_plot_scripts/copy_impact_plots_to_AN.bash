#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Define the source and destination directories
SOURCE_DIR=$SCRIPT_DIR"/../../plots/full_analysis/freeze/"
DEST_DIR=$SCRIPT_DIR"/../../AN_plots/full_analysis/freeze/"

# Check if the source file is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Define the file to copy
FILE="$1"

# Copy the file from the source to the destination
cp "$SOURCE_DIR$FILE" "$DEST_DIR"

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "File '$FILE' successfully copied to '$DEST_DIR'."
else
    echo "Failed to copy the file."
fi
