#!/usr/bin/env bash

# get cmdline args
# first set defaults
channel="all"
while getopts c: flag
do
    case "${flag}" in
        c) channel=${OPTARG}
    esac
done
echo ${channel}

# vars
# BASE_DIR="$(git rev-parse --show-toplevel)/EFTAnalysisFitting/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )

# test
# echo $BASE_DIR
echo $SCRIPT_DIR

# activate conda
# source $BASE_DIR/scripts/init_conda.sh

echo $(which python)

# run python script
#python $SCRIPT_DIR/split_yields.py -c ${channel}
python $SCRIPT_DIR/split_yields_v2.py -c ${channel}
