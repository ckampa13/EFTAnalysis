#!/usr/bin/bash

# arguments: 1 (optional): which level -- "c" or "f" (default); 2 (optional) -- which channel, e.g. "all" (default); 3 (optional) -- which dim, e.g. "dim8" (default)

if [[ -z "$1" ]]; then
    L="f"
else
    L=$1
fi

if [[ -z "$2" ]]; then
    CH="all"
else
    CH=$2
fi

if [[ -z "$3" ]]; then
    DIM="dim8"
else
    DIM=$3
fi

for i in $(seq 0 12);
do
    echo Making workspaces for clip index $i...
    python tools/make_workspaces.py -c $CH -d $DIM -t $L -v _clip_mVVV_$i
done
