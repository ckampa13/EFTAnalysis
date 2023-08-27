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
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )

# split yields
bash ${SCRIPT_DIR}/split_yields1.sh -c ${channel}

# first split yields using uproot (conda)
# bash ${SCRIPT_DIR}/split_yields1.sh -c ${channel}

# then update the errors in the new files (pyroot)
# bash ${SCRIPT_DIR}/split_yields2.sh -c ${channel}
