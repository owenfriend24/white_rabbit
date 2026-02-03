#!/usr/bin/env python

### Import required Python libraries ###
import numpy as np
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
import subprocess
import argparse
import pandas as pd

# ignore division by zero errors for NaN values when transforming to fisher's Z
np.seterr(divide='ignore', invalid='ignore')

### Import custom similarity function ###
from similarity_values_function import *
from wr_utils import get_mask_list

### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")

    # Required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    parser.add_argument("comparison", help="Comparison type (14, 1234)")
    parser.add_argument("masktype", help="Mask type (e.g., lat_hip_subregions, searchlight)")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()

### Main script execution ###
if __name__ == "__main__":
    args = get_args()

    ### Set up experiment info ###

    sbj = args.subject_id
    comparison = args.comparison
    masktype = args.masktype
    drop_run = args.drop_run

    expdir = '/corral-repl/utexas/prestonlab/whiterabbit_temp/'
    subjdir = os.path.join(expdir, f'sub-{sbj}')
    betadir = os.path.join(subjdir, 'betaseries')
    out_dir = os.path.join(subjdir, f'PS_{masktype}_{comparison}/')
    os.makedirs(out_dir, exist_ok=True)



    ### Validate masks for data analysis ###
    if masktype == 'b_hip_subregions':
        masks = get_mask_list.get_bilateral_hip_masks()
    elif masktype == 'lat_hip_subregions':
        masks = get_mask_list.get_lat_hip_masks()
    elif masktype == 'searchlight':
        cluster_dir = f"/corral-repl/utexas/prestonlab/whiterabbit_temp/sub-{sbj}/masks/sl_masks/"
        masks = get_mask_list.get_searchlight_masks(cluster_dir)
    else:
        raise ValueError('Invalid mask type')

    if comparison == '14':
        comp_file = f'{betadir}/sub-{sbj}_sl_meta_1v4.txt'
    elif comparison == 'all':
        comp_file = f'{betadir}/sub-{sbj}_sl_meta.txt'
    else:
        raise ValueError('no valid comparison provided! oh no!')

    if drop_run is not None:
        print('need to write the dropped run logic into the txt files!'
        # phase, run, triad, item = np.loadtxt(
        #     f'_{comp_file}_items_drop{drop_run}.txt',
        #     unpack=True
        )
    else:
        run, mini_block, context, item = np.loadtxt(comp_file, unpack=True)


    for mask in masks:
        print(f"running in mask {mask}")
        if masktype in ['b_hip_subregions', 'lat_hip_subregions']:
            slmask = f'{subjdir}/masks/hip_masks/{mask}.nii.gz'
        # elif masktype in ['lat_hip_subfields', 'b_hip_subfields']:
        #     slmask = f"{expdir}/ashs/masks/sub-{sbj}/subfield_masks/func/sub-{sbj}_{mask}.nii.gz"
        elif masktype == 'searchlight':
            slmask = f"/corral-repl/utexas/prestonlab/white_rabbit/sub-{sbj}/masks/sl_masks/{mask}.nii.gz"
        # elif masktype == 'searchlight_dilated':
        #     slmask = f"/corral-repl/utexas/prestonlab/temple/sub-{sbj}/masks/sl_masks/{mask}_dilated.nii.gz"

        # Load fMRI data
        if comparison == '14':
            ds = fmri_dataset(os.path.join(betadir, f'1v4_items.nii.gz'), mask=slmask)
        else:
            ds = fmri_dataset(os.path.join(betadir, f'all_items.nii.gz'), mask=slmask)

        ds.sa['run'] = run[:]
        ds.sa['mini_block'] = mini_block[:]
        ds.sa['context'] = context[:]
        ds.sa['item'] = item[:]

        niter = 1000 # doesn't do anything, need to update
        sl_func = similarity_values_function('correlation', 1, niter)

        # Obtain pattern similarity vals
        df = sl_func(ds)

        out_file_df = os.path.join(out_dir, f"{sbj}_PS_{comparison}_{mask}_full.csv")

        print(f"saving file to {out_file_df}")
        df.to_csv(out_file_df)

