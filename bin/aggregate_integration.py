#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from wr_utils import get_age_groups


def run(command):
    subprocess.run(command, shell=True)

def aggregate_csv_files(comparison, csv_files, master_dir, mask):
    aggregated_data = []

    for file_path in csv_files:
        file_path = Path(file_path)
        if file_path.exists():
            df = pd.read_csv(file_path)
            aggregated_data.append(df)
        else:
            print(f"no file found at {file_path}")

    if aggregated_data:
        master_df = pd.concat(aggregated_data, ignore_index=True)

        master_output_path = f"{master_dir}/aggregated_{comparison}_{mask}.csv"
        master_df.to_csv(master_output_path, index=False)
        print(f"Aggregated file saved at: {master_output_path}")
    else:
        print("No CSV files were found for aggregation.")

def is_processed (sub, comparison, master_dir, mask):
    ps_file = Path(f"{master_dir}/sub-{sub}/PS_{mask}_{comparison}/PS_{mask}_{comparison}_master.csv")
    print(f'checking for {ps_file}')
    return ps_file.exists()

def main(master_dir, comparison, mask, agg_file):
    subjects = get_age_groups.get_all_subjects()
    excludes = []

    # drop_runs = {
    #     "temple023": 6
    #     # "temple030": 6,
    #     # "temple070": 3,
    #     # # "temple115": 3,
    #     # "temple116": 5,
    # }
    ps_csv_files = []
    symmetry_csv_files = []

    for sub in subjects:
        if sub in excludes:
            continue

       # drop_run = drop_runs.get(sub)
       # drop_flag = f"--drop_run {drop_run} " if drop_run else ""

        sub_processed = is_processed(sub, comparison, master_dir, mask)

        if sub_processed:
            print(f"Already processed prepost for {sub}.")
        else:
            print(f"Processing prepost values for {sub}...")
            run(f"roi_similarity_values.py {sub} {comparison} {mask}")
            run(f"merge_ps_files.py {sub} {comparison} {mask}")
        ps_csv_files.append(
            f"{master_dir}/sub-{sub}/PS_{mask}_{comparison}/PS_{mask}_{comparison}_master.csv")

    if agg_file:
        aggregate_csv_files(comparison, ps_csv_files, master_dir, mask)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("master_dir", help="where folders containing .txt files for each comparison are stored")
    parser.add_argument("comparison", help="options: 14, 1234")
    parser.add_argument("mask", help="mask name e.g., b_hip_subregions, ifg_subregions, lat_hip_subfields, etc.")
    parser.add_argument("--agg_file", action=argparse.BooleanOptionalAction,
                        default=False, help="write aggregate file - boolean")

    args = parser.parse_args()
    main(args.master_dir, args.comparison, args.mask, args.agg_file)