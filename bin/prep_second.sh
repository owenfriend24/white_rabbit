#!/bin/bash

if [[ $# -lt 4 ]]; then
    echo "Usage: edit_first_fsf.sh template out_path subject fmriprep_dir"
    exit 1
fi

template=$1
out_path=$2
subject=$3
fm_dir=$4

# Load any necessary modules
module load python3/3.9.7

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/wr/wr_profile

# Move to the directory containing your Python script
cd /home1/09123/ofriend/analysis/wr/bin

mkdir /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/level2

for run in out_run1.feat out_run2.feat out_run3.feat out_run4.feat; do
mkdir /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/boundary/$run/reg
mkdir /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/source/$run/reg
mkdir /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/tempdist/$run/reg

cp "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/boundary/$run/mean_func.nii.gz" "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/boundary/$run/reg/standard.nii.gz"
cp "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/source/$run/mean_func.nii.gz"  "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/source/$run/reg/standard.nii.gz"
cp "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/tempdist/$run/mean_func.nii.gz"  "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/tempdist/$run/reg/standard.nii.gz"

cp "/home1/09123/ofriend/analysis/temple/univ/identity.mat" "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/boundary/$run/reg/example_func2standard.mat"
cp "/home1/09123/ofriend/analysis/temple/univ/identity.mat" "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/source/$run/reg/example_func2standard.mat"
cp "/home1/09123/ofriend/analysis/temple/univ/identity.mat" "/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-${subject}/univ/tempdist/$run/reg/example_func2standard.mat"
done

# Run your Python script
python first_level_fsfs.py $template $out_path $subject 5 222
