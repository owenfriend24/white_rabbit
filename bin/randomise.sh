#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 2 ]]; then
    echo "randomise_new.sh roi comp"
    exit 1
fi

roi=$1

if [[ $roi == 'b_hip' ]]; then
  grp_mask_path=/corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_func.nii.gz
elif [[ $roi == 'b_gray_func' ]]; then
  grp_mask_path=/corral-repl/utexas/prestonlab/temple/group_masks/gm/gm_binary/prob_mask.nii.gz
fi

mkdir -p /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/same_over_diff/randomise_out/
mkdir -p /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/diff_over_same/randomise_out/


randomise -i /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/same_over_diff/group_z.nii.gz \
-o /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/same_over_diff/randomise_out/cont_age \
-d /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/design/age_47.mat \
-t /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/design/age_47.con \
-m $grp_mask_path \
-n 5000 -x --uncorrp

randomise -i /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/same_over_diff/group_z.nii.gz \
-o /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/same_over_diff/randomise_out/group_mean \
-m $grp_mask_path \
-1 \
-n 5000 -x  --uncorrp

randomise -i /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/diff_over_same/group_z.nii.gz \
-o /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/diff_over_same/randomise_out/cont_age \
-d /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/design/age_47.mat \
-t /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/design/age_47.con \
-m $grp_mask_path \
-n 5000 -x --uncorrp

randomise -i /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/diff_over_same/group_z.nii.gz \
-o /corral-repl/utexas/prestonlab/whiterabbit_temp/randomise/mni_b_hip/diff_over_same/randomise_out/group_mean \
-m $grp_mask_path \
-1 \
-n 5000 -x  --uncorrp
