#!/bin/bash
#
# use feat to run first level analyses - specifically for runs 1 and 4 right now
#
if [[ $# -lt 2 ]]; then
    echo "Usage: run_first_levels.sh fmriprep_dir subject"
    exit 1
fi

fmriprep_dir=$1
subject=$2


for run in 1 2 3 4; do
    echo "running first level BOUNDARY analysis for sub ${subject}..."
    feat "${fmriprep_dir}/sub-${subject}/univ/boundary/sub-${subject}-boundary_run-0${run}.fsf"

    echo "running first level SOURCE analysis for sub ${subject}..."
    feat "${fmriprep_dir}/sub-${subject}/univ/source/sub-${subject}-source_run-0${run}.fsf"

    echo "running first level TEMPDIST analysis for sub ${subject}..."
    feat "${fmriprep_dir}/sub-${subject}/univ/tempdist/sub-${subject}-tempdist_run-0${run}.fsf"
done
