#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from temple_utils import get_age_groups


def run(command):
    subprocess.run(command, shell=True)

def aggregate_csv_files(comparison, csv_files, master_dir, mask, out_flag):
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

        master_output_path = f"{master_dir}/aggregated_{comparison}_{mask}_{out_flag}.csv"
        master_df.to_csv(master_output_path, index=False)
        print(f"Aggregated file saved at: {master_output_path}")
    else:
        print("No CSV files were found for aggregation.")

def is_processed (sub, comparison, master_dir, mask, measure):
    prepost_file = Path(master_dir) / f"prepost_{comparison}/sub-{sub}/sub-{sub}_{comparison}_{mask}_master.csv"
    symmetry_file = Path(master_dir) / f"symmetry_{comparison}/sub-{sub}/sub-{sub}_{comparison}_{mask}_master.csv"

    if measure == "both":
        return prepost_file.exists() and symmetry_file.exists()
    elif measure == "prepost":
        return prepost_file.exists()
    elif measure == "symmetry":
        return symmetry_file.exists()
    return False  # defaults to false

def main(measure, master_dir, comparison, mask, agg_file):
    subjects = get_age_groups.get_all_subjects()
    excludes = []

    drop_runs = {
        "temple023": 6
        # "temple030": 6,
        # "temple070": 3,
        # # "temple115": 3,
        # "temple116": 5,
    }
    integration_csv_files = []
    symmetry_csv_files = []

    for sub in subjects:
        if sub in excludes:
            continue

        drop_run = drop_runs.get(sub)
        drop_flag = f"--drop_run {drop_run} " if drop_run else ""

        sub_processed = is_processed(sub, comparison, master_dir, mask, measure)

        if measure in ["prepost", "both"] and not sub_processed:
            print(f"Processing prepost values for {sub}...")
            run(f"integration_prepost_values.py {drop_flag}{sub} {comparison} {mask}")
            run(f"merge_integration.py {sub} {master_dir} {comparison} {mask}")
        elif measure in ["prepost", "both"] and sub_processed:
            print(f"Already processed prepost for {sub}.")

        integration_csv_files.append(
            f"{master_dir}/prepost_{comparison}/sub-{sub}/sub-{sub}_{comparison}_{mask}_master.csv")

        if measure in ["symmetry", "both"] and not sub_processed:
            bwd_comp = comparison[::-1]
            print(f"Processing symmetry values for {sub}...")
            run(f"symmetry_prepost_values.py {drop_flag}{sub} {comparison} {mask}")
            run(f"symmetry_prepost_values.py {drop_flag}{sub} {bwd_comp} {mask}")
            run(f"merge_symmetry.py {sub} {master_dir} {comparison} {mask}")
        elif measure in ["symmetry", "both"] and sub_processed:
            print(f"Already processed symmetry for {sub}.")

        symmetry_csv_files.append(
            f"{master_dir}/symmetry_{comparison}/sub-{sub}/sub-{sub}_{comparison}_{mask}_master.csv")

    if agg_file:
        if measure in ["prepost", "both"]:
            aggregate_csv_files(comparison, integration_csv_files, master_dir, mask,"prepost")

        if measure in ["symmetry", "both"]:
            aggregate_csv_files(comparison, symmetry_csv_files, master_dir, mask, "symmetry")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("measure", help="prepost, symmetry, both")
    parser.add_argument("master_dir", help="where folders containing .txt files for each comparison are stored")
    parser.add_argument("comparison", help="options: AB, BC, AC")
    parser.add_argument("mask", help="mask name e.g., b_hip_subregions, ifg_subregions, lat_hip_subfields, etc.")
    parser.add_argument("--agg_file", action=argparse.BooleanOptionalAction,
                        default=False, help="write aggregate file - boolean")

    args = parser.parse_args()
    main(args.measure, args.master_dir, args.comparison, args.mask, args.agg_file)