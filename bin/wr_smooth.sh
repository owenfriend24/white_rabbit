#!/bin/bash
#
# Smooth functional data

if [[ $# -lt 4 ]]; then
    echo "Usage: temple_smooth.sh fmriprep_dir fs_dir subject task"
    exit 1
fi

export PATH=/home1/09123/ofriend/analysis/wr/bin:$PATH
source /home1/09123/ofriend/analysis/wr/wr_profile
fmriprep_dir=$1
fs_dir=$2
subject=$3
task=$4


for run in 1 2 3 4; do
    echo "Smoothing run ${run}..."


    smooth_susan \
        "${fmriprep_dir}/sub-${subject}/func/skullstripped_T1/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss.nii.gz" \
        "${fs_dir}/sub-${subject}/mri/out/brainmask_func_dilated.nii.gz" \
        4 \
        "${fmriprep_dir}/sub-${subject}/func/skullstripped_T1/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz"
    
    echo "Finished smoothing run ${run}!"
    
done
