#!/bin/env bash
#
# transform searchlight outputs to template space for across participant comparisons

if [[ $# -lt 1 ]]; then
    echo "Usage:  sl_to_mni.sh sub corr comp roi (e.g., sl_to_mni.sh wr200 CORR 14 b_hip)"
    exit 1
fi

sub=$1
corr=$2
comp=$3
roi=$4

sl_dir=${corr}/sub-${sub}/searchlight_${comp}/
mkdir -p ${sl_dir}/mni/

for zmap in ${sl_dir}/*${roi}*; do
  fname=$(basename "${zmap}")
  antsApplyTransforms -d 3 \
    -i "${zmap}" \
    -o "${sl_dir}/mni/${fname}" \
    -r "/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz" \
    -t "${corr}/sub-${sub}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt"
done



