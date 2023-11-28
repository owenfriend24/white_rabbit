#!/bin/bash
#
# Run heudiconv to convert raw data for one subject.

if [[ $# -lt 4 ]]; then
    echo "Usage: wr_heudiconv.sh subject raw_dir heuristic bids_dir"
    exit 1
fi

subject=$1
raw_dir=$2
heuristic=$3
bids_dir=$4

subj_id=$subject
subj_raw_dir=$raw_dir/$subject

if [[ ! -d $subj_raw_dir ]]; then
    echo "Error: raw directory not found: $subj_raw_dir"
    exit 1
fi

if [[ ! -f $heuristic ]]; then
    echo "Error: heuristic file does not exist: $heuristic"
    exit 1
fi

image=/work/03206/mortonne/software/images/heudiconv-0.11.3.sif
module load tacc-singularity


singularity run "$image" \
    -s "$subject" \
    -f "$heuristic" \
    -b \
    -o "$bids_dir" \
    --minmeta \
    # for skyra, below line needs to be --files "$subj_raw_dir"/*/*.* \
    --files "$subj_raw_dir"/*.* \
    --overwrite 

fi
