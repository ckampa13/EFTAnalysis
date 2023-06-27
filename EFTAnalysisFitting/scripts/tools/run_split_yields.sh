#!/usr/bin/env bash

# vars
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )

# first split yields using uproot (conda)
bash ${SCRIPT_DIR}/split_yields1.sh

# then update the errors in the new files (pyroot)
bash ${SCRIPT_DIR}/split_yields2.sh
