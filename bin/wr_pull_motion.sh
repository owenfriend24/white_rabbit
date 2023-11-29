#!/bin/bash
#
# Pull white rabbit bids behavior files with .tsv extension.

if [[ $# -lt 2 ]]; then
    echo "Usage:   wr_pull_motion.sh src dest [rsync flags]"
    exit 1
fi

src=$1
dest=$2
shift 2

rsync -azvu "$src" "$dest" \
    --include="sub-*/*/*.tsv" \
    --exclude="sub-*/*/*.nii.gz" \
    --exclude="der*" \
    --exclude="*.json" \
    --exclude="*.out" \
    --exclude="fmap" \
    --exclude="sourcedata" \
    --exclude="anat" \
    --exclude=".heudiconv" \
    --exclude="*.gii" \
    --exclude="*.txt" \
    --exclude="*.svg" \
    --exclude="*.html" \
    --exclude="CHANGES" \
    --exclude="README" \
    --exclude="*.label" \
    --exclude="*.mgz" \
    --exclude="*.nii.gz" \
    --exclude="*.gz"
