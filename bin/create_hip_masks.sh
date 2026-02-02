#!/bin/bash
#
# create hippocampus masks from custom MNI

if [[ $# -lt 2 ]]; then
    echo "create_hip_masks.sh sub corall_dir"
    exit 1
fi

sub=$1
corr=$2

mkdir -p ${corr}/sub-${sub}/masks/hip_masks/

  for mask in 11m 14c 14r 25 32pl b_erc b_phc b_prc b_hip b_hip_ant b_hip_body b_hip_post l_hip l_hip_ant l_hip_body l_hip_post r_hip r_hip_ant r_hip_body r_hip_post; do

  antsApplyTransforms -d 3 \
    -i /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz \
    -o ${corr}/sub-${sub}/masks/hip_masks/func-${mask}.nii.gz \
    -r ${corr}/sourcedata/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
    -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt,1] \
    -t ${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz \
    -n NearestNeighbor

done

