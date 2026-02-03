#!/usr/bin/env python

import os
import argparse
import pandas as pd
from wr_utils import get_age_groups, get_mask_list # need to actually set these up

def create_subject_file(subject, comparison, mask):
    group = get_age_groups.get_subject_group(subject)
    age = get_age_groups.get_subject_age(subject)

    if mask == 'b_hip_subregions':
        masks = get_mask_list.get_bilateral_hip_masks()
    elif mask == 'lat_hip_subregions':
        masks = get_mask_list.get_lat_hip_masks()
    elif mask == 'searchlight':
        cluster_dir = f"/corral-repl/utexas/prestonlab/whiterabbit_temp/sub-{subject}/masks/sl_masks/"
        masks = get_mask_list.get_searchlight_masks(cluster_dir)
    else:
        raise ValueError('Invalid mask type')

    sub_dir = f'/corral-repl/utexas/prestonlab/whiterabbit_temp/sub-{subject}/PS_{mask}_{comparison}/'

    roi_dfs = []

    column_order = ['subject', 'age', 'age_group', 'roi', 'compare_type',
        'run', 'mini_block', 'trial_1', 'trial_2', 'comparison', 'pattern_similarity']

    for m in masks:
        ps_file = os.path.join(sub_dir, f'{subject}_PS_{comparison}_{m}_full.csv')

        if os.path.exists(ps_file):
            temp_df = pd.read_csv(ps_file)
            temp_df = temp_df[['comparison', 'run_1', 'mini_block_1', 'item_1', 'item_2', 'pattern_similarity']]

            # match master format
            temp_df = temp_df.rename(columns={
                'run_1': 'run',
                'mini_block_1': 'mini_block',
                'item_1': 'trial_1',
                'item_2': 'trial_2'
            })

            # 2. Add metadata
            temp_df['subject'] = subject
            temp_df['age'] = age
            temp_df['age_group'] = group
            temp_df['roi'] = m
            temp_df['compare_type'] = str(comparison)

            temp_df = temp_df[column_order]

            roi_dfs.append(temp_df)
        else:
            print(f"Warning: File not found for mask {m}")

    if roi_dfs:
        comp_data = pd.concat(roi_dfs, ignore_index=True)
    else:
        comp_data = pd.DataFrame()
    return comp_data

def main(subject, comparison, mask):
    out_file =  f'/corral-repl/utexas/prestonlab/whiterabbit_temp/sub-{subject}/PS_{mask}_{comparison}/PS_{mask}_{comparison}_master.csv'
    df = create_subject_file(subject, comparison, mask)
    df.to_csv(out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="e.g., temple100")
    parser.add_argument("comparison", help="options: 14, 1234")
    parser.add_argument("mask", help="mask name e.g., lat_hip_subregions, searchlight, etc.")
    args = parser.parse_args()
    main(args.subject, args.comparison, args.mask)