#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo "Usage: prep_func_data.sh freesurfer_dir fmriprep_dir subject task num_runs"
    exit 1
fi

fsdir=$1
fmdir=$2
subject=$3
task=$4
num_runs=$5

# Load any necessary modules
module load python3/3.9.7

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/wr/wr_profile

# Move to the directory containing your Python script
cd /home1/09123/ofriend/analysis/wr/bin

# Run your Python script
python prep_func_data.py $fsdir $fmdir $subject $task $num_runs
mni_transforms.sh $fmdir $subject
wr_smooth.sh $fmdir $fsdir $subject imagine