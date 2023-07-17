#!/usr/bin/env bash

# get cmdline args
# first set defaults
WC="cW"
while getopts w: flag
do
    case "${flag}" in
        w) WC=${OPTARG}
    esac
done
echo ${WC}

# vars
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )

# first split yields using uproot (conda)
bash ${SCRIPT_DIR}/split_yields1.sh -w ${WC}

# then update the errors in the new files (pyroot)
bash ${SCRIPT_DIR}/split_yields2.sh -w ${WC}
