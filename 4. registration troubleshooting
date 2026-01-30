# works but looks a little less good
```
 antsApplyTransforms -d 3 -i $WORK/wr/mni_rois/b_hip.nii.gz -o ./mni_rois/b_hip.nii.gz -r /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/anat/sub-wr201_T1w_ss.nii.gz -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_InverseWarp.nii.gz] -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_Affine.txt, 1]
 ```

 # works and looks better but doesn't have right functional dimensions
 ```
 antsApplyTransforms -d 3 -i $WORK/wr/mni_rois/b_hip.nii.gz -o ./mni_rois/b_hip_func.nii.gz -r /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/anat/sub-wr201_T1w_ss.nii.gz -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_InverseWarp.nii.gz] -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_Affine.txt, 1] -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/mask_to_func_ref_Affine.txt]
 ```

# masks should be NN
```
antsApplyTransforms -d 3 -n NearestNeighbor -i $WORK/wr/mni_rois/b_hip.nii.gz -o ./mni_rois/b_hip_nn.nii.gz -r /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/anat/sub-wr201_T1w_ss.nii.gz -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_InverseWarp.nii.gz] -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_Affine.txt, 1]
 ```

# not outputting? maybe memory issue? launch as job?
```
  antsApplyTransforms -d 3 -n NearestNeighbor -i $WORK/wr/mni_rois/b_hip.nii.gz -o ./mni_rois/b_hip_nn.nii.gz -r /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/anat/sub-wr201_T1w_ss.nii.gz -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_InverseWarp.nii.gz] -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/native_to_MNI_Affine.txt, 1] -t [/scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr201/transforms/mask_to_func_ref_Affine.txt] ```
```

the inverse transformations aren't looking right, going to try to directly create transforms for MNi to functional
```
ANTS 3 -m MI[ {fixed image (space we're registering to)}, {moving image (image we're moving into fixed image's space)},1,32] -o {outpath} --rigid-affine true -i 0

ANTS 3 -m MI[$FM/sub-wr206/func/sub-wr206_task-imagine_run-01_boldref.nii.gz, $WORK/wr/mni_rois/b_hip.nii.gz,1,32] -o $FM/sub-wr206/transforms/direct_mni_func --rigid-affine true -i 0
ANTS 3 -m MI[$FM/sub-wr206/func/sub-wr206_task-imagine_run-01_boldref.nii.gz, $WORK/wr/mni_rois/b_hip.nii.gz,1,32] -o $FM/sub-wr206/transforms/direct_mni_func --rigid-affine true -i 0
ANTS 3 -m MI[$FM/sub-wr206/func/sub-wr206_task-imagine_run-01_boldref.nii.gz, /corral-repl/utexas/prestonlab/xmaze/batch/templates/MNI152_T1_1mm_brain.nii.gz,1,32] -o $FM/sub-wr206/transforms/direct_mni_func_full_MNI --rigid-affine true -i 0
```

```
not gonna work because the above doesn't output a warp just an affine
antsApplyTransforms -d 3 -i "$WORK/wr/mni_rois/b_hip.nii.gz" -o "$FM/sub-wr206/transforms/direct_MNI_mask.nii.gz" -n NearestNeighbor -r $FM/sub-wr206/func/sub-wr206_task-imagine_run-01_boldref.nii.gz -t "$FM/sub-wr206/transforms/direct_mni_func_Warp.nii.gz" -t "$FM/sub-wr206/transforms/direct_mni_func_Affine.txt"
antsApplyTransforms -d 3 -i "$WORK/wr/mni_rois/b_hip.nii.gz" -o "$FM/sub-wr206/transforms/direct_MNI_mask.nii.gz" -n NearestNeighbor -r $FM/sub-wr206/func/sub-wr206_task-imagine_run-01_boldref.nii.gz -t "$FM/sub-wr206/transforms/direct_mni_func_full_MNI_Warp.nii.gz" -t "$FM/sub-wr206/transforms/direct_mni_func_full_MNI_Affine.txt"



antsApplyTransforms -d 3 -i $WORK/wr/mni_rois/b_hip.nii.gz -o $FM/sub-wr206/transforms/direct_MNI_mask.nii.gz -t $FM/sub-wr206/transforms/direct_mni_funcAffine.txt -r $FM/sub-wr206/func/sub-wr206_task-imagine_run-01_boldref.nii.gz

# this one looks pretty good; will need to run for all subjects to confirm.
antsApplyTransforms -d 3 -i $WORK/wr/mni_rois/b_hip.nii.gz -o $FM/sub-wr206/transforms/direct_MNI_full_mask.nii.gz -t $FM/sub-wr206/transforms/direct_mni_func_full_MNIAffine.txt -r $FM/sub-wr206/func/sub-wr206_task-imagine_run-01_boldref.nii.gz


set up for group in mni_masks_to_func.sh, re created rep_sup.py (will need to rerun for all subs)
