#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: copy_prep.sh subject"
    exit 1
fi

subject=$1

cp /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}.html /corral-repl/utexas/prestonlab/whiterabbit_temp/
cp -R /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/ /corral-repl/utexas/prestonlab/whiterabbit_temp/
cp -R /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sourcedata/freesurfer/sub-${subject} /corral-repl/utexas/prestonlab/whiterabbit_temp/sourcedata/freesurfer/
