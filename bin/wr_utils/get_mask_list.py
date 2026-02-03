#!/usr/bin/env python

import os

def get_lat_hip_masks():
    return ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body',
                 'func-l_hip', 'func-l_hip_ant', 'func-l_hip_post', 'func-l_hip_body',
                 'func-r_hip', 'func-r_hip_ant', 'func-r_hip_post', 'func-r_hip_body']

def get_bilateral_hip_masks():
    return ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body']

def get_lat_subfield_masks():
    return ['CA1_mask_B_func', 'CA1_mask_L_func', 'CA1_mask_R_func',
                 'CA23DG_mask_B_func', 'CA23DG_mask_L_func', 'CA23DG_mask_R_func',
                 'posthipp_mask_B_func', 'posthipp_mask_L_func', 'posthipp_mask_R_func',
                 'subiculum_mask_B_func', 'subiculum_mask_L_func', 'subiculum_mask_R_func']

def get_bilateral_subfield_masks():
    return ['CA1_mask_B_func', 'CA23DG_mask_B_func', 'posthipp_mask_B_func', 'subiculum_mask_B_func']

def get_searchlight_masks(cluster_dir):
    masks = []
    for f in os.listdir(cluster_dir):
        if f.endswith('.nii') or f.endswith('.nii.gz'):
            name = f.replace('.nii.gz', '').replace('.nii', '')
            masks.append(name)
    return masks
