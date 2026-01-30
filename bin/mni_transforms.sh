#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: mni_transforms.sh fmriprep_dir subject"
    exit 1
fi

fmriprep_dir=$1
subject=$2


fslmaths "${fmriprep_dir}/sub-${subject}/anat/sub-${subject}_desc-preproc_T1w.nii.gz" -mas "${fmriprep_dir}/sub-${subject}/anat/sub-${subject}_desc-brain_mask.nii.gz" "${fmriprep_dir}/sub-${subject}/anat/sub-${subject}_T1w_ss.nii.gz"

# create transforms from anatomical space to MNI space
ANTS 3 -m CC[/corral-repl/utexas/prestonlab/xmaze/batch/templates/MNI152_T1_1mm_brain.nii.gz, "${fmriprep_dir}/sub-${subject}/anat/sub-${subject}_T1w_ss.nii.gz",1,5] -t SyN[0.25] -r Gauss[3,0] -o "${fmriprep_dir}/sub-${subject}/transforms/native_to_MNI_" -i 30x90x20 --use-Histogram-Matching --number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000

WarpImageMultiTransform 3 "${fmriprep_dir}/sub-${subject}/anat/sub-${subject}_T1w_ss.nii.gz" "${fmriprep_dir}/sub-${subject}/anat/sub-${subject}_MNI_ss.nii.gz" -R /corral-repl/utexas/prestonlab/xmaze/batch/templates/MNI152_T1_1mm_brain.nii.gz "${fmriprep_dir}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" "${fmriprep_dir}/sub-${subject}/transforms/native_to_MNI_Affine.txt"







