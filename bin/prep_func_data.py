#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse

def run(command):
    #print(f"Running command: {command}")
    subprocess.run(command, shell=True)

def extract_fs(fs_dir, sub):
    fs = Path(fs_dir)
    src = fs/f'sub-{sub}/mri'
    run(f'mkdir {src}/out') 
    run('module load freesurfer')
    dest = src/'out'
    
    src_names = ['orig', 'brainmask', 'aparc+aseg',
                 'aparc.a2009s+aseg', 'aparc.DKTatlas+aseg']
    dest_names = ['orig', 'orig_brain_auto', 'aparc+aseg',
                   'aparc.a2009s+aseg', 'aparc.DKTatlas+aseg']
    
    
    print('converting freesurfer .mgz images to Nifti')
    for i in range(len(src_names)):
        src_file = src / f'{src_names[i]}.mgz'  
        dest_file = dest / f'{dest_names[i]}.nii.gz'

        if not os.path.exists(src_file):
            run(f'echo FreeSurfer file not found: {src_file}')
            continue

        # convert to Nifti
        run(f'mri_convert {src_file} {dest_file}')

        # fix orientation
        run(f'fslreorient2std {dest_file} {dest_file}')

    # use the FS parcelation to get an improved brain extraction
    
    print('extracting brain with automatic mask')
    # mask for original brain extraction
    brain_auto = dest/'orig_brain_auto'
    mask_auto = dest/'brainmask_auto'
    run(f'fslmaths {brain_auto} -thr 0.5 -bin {mask_auto}')
    
    print('updating mask with freesurfer parcellations')
    # smooth and threshold the identified tissues; fill any remaining holes
    parcel = dest/'aparc+aseg'
    mask_surf = dest/'brainmask_surf'
    run(f'fslmaths {parcel} -thr 0.5 -bin -s 0.25 -bin -fillh26 {mask_surf}')
    # take intersection with original mask (assumed to include all cortex,
    # so don't want to extend beyond that)
    mask = dest/'brainmask'
    run(f'fslmaths {mask_surf} -mul {mask_auto} -bin {mask}')
    print(f'created brain mask image at {mask}')

    
    # create a brain-extracted image based on the orig image from
    # freesurfer (later images have various normalization things done that
    # won't match the MNI template as well)
    
    orig = dest/'orig'
    output = dest/'orig_brain'
    run(f'fslmaths {orig} -mas {mask} {output}')
    print(f'created skull stripped anatomical at {output}')

    # cortex
    cort_out = dest/'ctx'
    run(f'fslmaths {parcel} -thr 1000 -bin {cort_out}')
    print(f'created cortex image at {output}')

    # cerebral white matter
    lwm_out = dest/'l_wm'
    rwm_out = dest/'r_wm'
    wm_out = dest/'wm'
    run(f'fslmaths {parcel} -thr 2 -uthr 2 -bin {lwm_out}')
    run(f'fslmaths {parcel} -thr 41 -uthr 41 -bin {rwm_out}')
    run(f'fslmaths {lwm_out} -add {rwm_out} -bin {wm_out}')
    print(f'created white matter images at {wm_out}')

    
def extract_func(fs_dir, fmriprep_dir, sub, task, num_runs): 
    # set up freesurfer paths and functional data paths
    fs_dir = Path(fs_dir)
    src = fs_dir / f'sub-{sub}/mri'
    fmriprep_dir = Path(fmriprep_dir)/f'sub-{sub}'
    func_dir = fmriprep_dir /'func'
    
    # create directory to store affine transform files
    run(f'mkdir {fmriprep_dir}/transforms')
    
    # create directory within func to store skullstripped func data
    run(f'mkdir {func_dir}/skullstripped_T1')
    dest = func_dir / 'skullstripped_T1'
    
    # path to mask created from freesurfer output
    highres_mask = fs_dir / f'sub-{sub}/mri/out/brainmask'
    
    # output path for mask transformed to functional space
    mask_func = fs_dir / f'sub-{sub}/mri/out/brainmask_func'
    
    # functional data to reference in transform for dimensions/space
    ref_func = func_dir / f'sub-{sub}_task-{task}_run-01_space-T1w_boldref'
    
    # create affine txt file to go from anatomical to functional space
    run(f'ANTS 3 -m MI[ {ref_func}.nii.gz, {highres_mask}.nii.gz,1,32] -o {fmriprep_dir}/transforms/mask_to_func_ref_ --rigid-affine true -i 0')
    print('created affine file')
    
    # apply affine file to transform mask from T1 anatomical to T1 functional space to match functional data's dimensions
    run(f'antsApplyTransforms -d 3 -i {highres_mask}.nii.gz -o {mask_func}.nii.gz -r {ref_func}.nii.gz -t {fmriprep_dir}/transforms/mask_to_func_ref_Affine.txt')
    print('transformed mask to functional space')
    
    
    run(f'fslmaths {mask_func}.nii.gz -kernel sphere 3 -dilD {mask_func}_dilated.nii.gz')
    print('dilated mask')
    
    # skullstrip the functional data
    for func_run in range(1, num_runs +1):
        print(f'attempting to run: fslmaths {func_dir}/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold.nii.gz -mas {mask_func}_dilated.nii.gz {func_dir}/skullstripped_T1/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold_ss.nii.gz')
        
        run(f'fslmaths {func_dir}/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold.nii.gz -mas {mask_func}_dilated.nii.gz {func_dir}/skullstripped_T1/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold_ss.nii.gz')
        print(f'skullstripped run {func_run}')

  #     fslmaths /scratch/09123/ofriend/temple/skyra_prepro/derivatives/fmriprep/sub-temple029/func/sub-temple029_task-collector_run-01_space-T1w_desc-preproc_bold.nii.gz -mas /scratch/09123/ofriend/temple/skyra_prepro/derivatives/fmriprep/sourcedata/freesurfer/sub-temple029/mri/out/brainmask_func_dilated.nii.gz /scratch/09123/ofriend/temple/skyra_prepro/derivatives/fmriprep/sub-temple029/func/skullstripped_T1/workplz.nii.gz
        
# Function to smooth functional data with a 4.0 FWHM kernel
def smooth_func(fs_dir, fmriprep_dir, sub, task, num_runs):
    fs_dir = Path(fs_dir)
    mask = fs_dir / f'sub-{sub}/mri/out/brainmask_func.nii.gz'
    func_dir = Path(fmriprep_dir) / f'sub-{sub}/func'
    kernel = 4.0
    
    for func_run in range(1, num_runs + 1):
        func_input = func_dir / f'skullstripped_T1/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold_ss.nii.gz'
        func_output = func_dir / f'skullstripped_T1/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz'
        run(f'smooth_susan {func_input} {mask} {kernel} {func_output}')

def main(fs_dir, fmriprep_dir, sub, task, num_runs):
    run('source /home1/09123/ofriend/analysis/temple/profile')
    extract_fs(fs_dir, sub)
    print(f'\n\nMASK EXTRACTED FOR SUB-{sub}\n\n')
    extract_func(fs_dir, fmriprep_dir, sub, task, num_runs)
    print(f'\n\nSKULLSTRIPPING COMPLETE FOR SUB-{sub}\n\n')
   # smooth_func(fs_dir, fmriprep_dir, sub, task, num_runs)
   # print(f'\n\nSMOOTHING COMPLETE FOR SUB-{sub}\n\n')
          
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fs_dir", help="freesurfer directory")
    parser.add_argument("fmriprep_dir", help="fmriprep derivatives directory")
    parser.add_argument("sub", help="subject number; include full templeXXX")
    parser.add_argument("task", help="task_name")
    parser.add_argument("num_runs", help="number of runs to skullstrip")
    args = parser.parse_args()
    main(args.fs_dir, args.fmriprep_dir, args.sub, args.task, int(args.num_runs))
