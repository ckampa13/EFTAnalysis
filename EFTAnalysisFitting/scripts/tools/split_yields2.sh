#!/usr/bin/env bash

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
# FIXME! Add command line arguments to shell script (different WC)
python3 $SCRIPT_DIR/split_yields_bin_errors.py
