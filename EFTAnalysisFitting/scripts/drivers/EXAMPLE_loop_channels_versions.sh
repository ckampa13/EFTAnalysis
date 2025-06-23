#!/bin/bash
THIS_DIR="$(pwd)/"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}"  )" &> /dev/null && pwd  )
VDICT_DIR=$(realpath "${SCRIPT_DIR}/../")

echo "VDICT_DIR = ${VDICT_DIR}"

# Adjust PYTHONPATH if needed, or run from same directory
while read channel version; do
    echo "Running for channel=$channel, version=$version"
    # PUT COMMANDS HERE
done < <(python -c "
import sys
sys.path.append('${VDICT_DIR}')
from CONFIG_VERSIONS import versions_dict
for ch, meta in versions_dict.items():
    print '%s %s' % (ch, meta[\"v\"])
")
