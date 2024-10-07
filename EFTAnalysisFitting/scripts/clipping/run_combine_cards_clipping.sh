#!/usr/bin/bash

for i in $(seq 0 12);
do
    echo Combining cards for clip index $i...
    python tools/combine_cards.py -v _clip_mVVV_$i -d clipping
done
