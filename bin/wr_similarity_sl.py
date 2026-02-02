#!/usr/bin/env python
import subprocess

### import python libraries needed for the analysis ###
import numpy as np
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
import sys
from random import sample
from mvpa2.datasets.mri import *
from mvpa2.mappers.detrend import *
from mvpa2.mappers.zscore import *
from mvpa2.clfs.svm import *
from mvpa2.generators.partition import *
from mvpa2.measures.base import *
from mvpa2.measures import *
from mvpa2.measures.searchlight import *
from mvpa2.misc.stats import *
from mvpa2.base.node import *
from mvpa2.clfs.meta import *
from mvpa2.clfs.stats import *
from mvpa2.featsel.base import *
from mvpa2.featsel.helpers import *
from mvpa2.generators.permutation import *
from mvpa2.generators.base import *
from mvpa2.mappers.fx import *
from mvpa2.measures.anova import *
from mvpa2.base.dataset import *
import sys
import subprocess
import argparse

### import custom searchlight function ###
from searchlight_function_byrun import *

### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")
    # Required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., wr200)")
    parser.add_argument("comparison", help="Comparison type (e.g., 14, 1234)")
    parser.add_argument("masktype", help="Mask type (e.g., whole_brain)")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()

### Main script execution ###
if __name__ == "__main__":
    args = get_args()
    sbj = args.subject_id
    comparison = args.comparison
    masktype = args.masktype
    drop_run = args.drop_run

    expdir = '/corral-repl/utexas/prestonlab/whiterabbit_temp/'
    subjdir = os.path.join(expdir, f'sub-{sbj}')
    betadir = os.path.join(subjdir, 'betaseries')
    out_dir = os.path.join(subjdir, f'searchlight_{comparison}/')
    os.makedirs(out_dir, exist_ok=True)

    # don't think i'll need this
    niter= 1000

    ### masks for data to analyze ###
    if masktype == 'gm':
        masks = ['b_gray_func']
    elif masktype == 'whole_brain':
        masks = ['brainmask_func_dilated']
    elif masktype == 'hippocampus':
        masks = ['b_hip', 'l_hip', 'r_hip']

    if comparison == '14':
        comp_file = f'{betadir}/sub-wr261_sl_meta_1v4.txt'
    elif comparison == 'all':
        comp_file = f'{betadir}/sub-wr261_sl_meta.txt'
    else:
        raise ValueError('no valid comparison provided! oh no!')

    run, mini_block, context, item = np.loadtxt(comp_file, unpack=True)

    # # update for missing run ppts later
    # else:
    #     # Load phase, run, triad, and item data
    #     phase, run, triad, item = np.loadtxt(
    #         f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comp_file}_items.txt',
    #         unpack=True
    #     )

    for mask in masks:
        if masktype == 'gm':
            slmask = f'{expdir}/sourcedata/freesurfer/sub-{sbj}/mri/b_gray_func.nii.gz'
        elif masktype == 'whole_brain':
            slmask = f'{expdir}/sourcedata/freesurfer/sub-{sbj}/mri/out/brainmask_func_dilated.nii.gz'
        elif masktype == 'hippocampus':
            slmask = f'{expdir}/sub-{sbj}/masks/hip_masks/func-{mask}.nii.gz'

        if comparison == '14':
            ds = fmri_dataset(os.path.join(betadir, f'1v4_items.nii.gz'), mask=slmask)
        else:
            ds = fmri_dataset(os.path.join(betadir, f'all_items.nii.gz'), mask=slmask)

        ds.sa['run'] = run[:]
        ds.sa['mini_block'] = mini_block[:]
        ds.sa['context'] = context[:]
        ds.sa['item'] = item[:]

        sl_func = searchlight_function_byrun('correlation', 1, niter)

# # choose the function based on the comparison as some sl logic changes by comparison
#         if comparison == 'AC':
#             if drop_run is not None:
#                 sl_func = searchlight_AC_shuffle_droprun('correlation', 1, niter)
#             else:
#                 sl_func = searchlight_function_AC_shuffle('correlation', 1, niter)
#         elif comparison == 'ABC':
#             if drop_run is not None:
#                 sl_func = searchlight_adjacent_droprun('correlation', 1, niter)
#             else:
#                 sl_func = searchlight_function_adjacent('correlation', 1, niter)
#         elif comparison == 'AC_differentiation':
#             if drop_run is not None:
#                 sl_func = searchlight_AC_differentiation_droprun('correlation', 1, niter)
#             else:
#                 sl_func = searchlight_function_AC_differentiation('correlation', 1, niter)
#         else:
#             if drop_run is not None:
#                 sl_func = searchlight_function_prepost_droprun('correlation', 1, niter)
#             else:
#                 sl_func = searchlight_function_prepost('correlation', 1, niter)
        #run the searchlight

        sl = sphere_searchlight(sl_func,radius = 3)
        same_over_diff = sl(ds)
        diff_over_same = same_over_diff.copy()
        diff_over_same.samples = -same_over_diff.samples

        #save out map
        subjoutfile = f'{out_dir}/{sbj}_same_over_diff_{comparison}_{mask}_z.nii.gz' #z-score computed within searchlight
        map2nifti(ds, same_over_diff.samples).to_filename(subjoutfile)

        subjoutfile = f'{out_dir}/{sbj}_diff_over_same_{comparison}_{mask}_z.nii.gz'  # z-score computed within searchlight
        map2nifti(ds, diff_over_same.samples).to_filename(subjoutfile)
