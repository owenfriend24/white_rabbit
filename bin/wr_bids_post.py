#!/usr/bin/env python
# 
# Apply post-processing to a BIDS exported dataset.

import os
import sys
import stat
import json
import argparse
import pandas as pd
from glob import glob
from bids import BIDSLayout

def fix_dict(j):
    if 'time' in j and 'samples' in j['time']:
        if 'DataSetTrailingPadding' in j['time']['samples']:
            del j['time']['samples']['DataSetTrailingPadding']

    if 'global' in j:
        if 'slices' in j['global']:
            if 'DataSetTrailingPadding' in j['global']['slices']:
                del j['global']['slices']['DataSetTrailingPadding']
        if 'const' in j['global']:
            if 'DataSetTrailingPadding' in j['global']['const']:
                del j['global']['const']['DataSetTrailingPadding']


def load_json(file):
    with open(file, 'r') as f:
        j = json.load(f)
    return j


def get_files(data_dir, subj_id):
    '''Get subject specific files from bids dir'''
    files = glob(f'{data_dir}/sub-{subj_id}/*/*.json')
    if len(files) < 1:
        print(f'No files found for subject {subj_id}')
        sys.exit()
    return files


def sort_files_by_acquisition(data_dir, subj_id):
    '''Sort files by acquisition time'''

    # get files
    files = get_files(data_dir, subj_id)

    # pandas and sort
    df_list = []
    for file in files:
        j = load_json(file)
        fn = file.split('/')[-1].split('.')[0]
        acq = j['AcquisitionTime']
        df = pd.DataFrame({'Filename': [fn], 'AcquisitionTime': [acq]})
        df_list.append(df.copy())

    df = pd.concat(df_list)
    df = df.sort_values('AcquisitionTime')
    return df


# ...

def get_fieldmap_mapping(data_dir, subj_id):
    '''Generate Fieldmap mapping to bold runs'''
    
    # get sorted files
    df = sort_files_by_acquisition(data_dir, subj_id)

    # create fieldmap:runs(list) structure
    fieldmap_dict = dict()
    fieldmap_run_list = list()
    old_fieldmap_run_num = 1
    new_fieldmap_run_num = None  # Initialize new_fieldmap_run_num here

    for _, row in df.iterrows():
        run_id = row['Filename'].split('_')[-1]
        # identify fieldmap files
        if (run_id[:3] == 'epi'):
            new_fieldmap_run_num = int(row['Filename'].split('_')[2].split('-')[-1])

            # if new fieldmap run number, save out runs and create a new empty run list
            if old_fieldmap_run_num != new_fieldmap_run_num:
                fieldmap_dict[old_fieldmap_run_num] = fieldmap_run_list
                fieldmap_run_list = list()
                old_fieldmap_run_num = new_fieldmap_run_num

        elif run_id == 'bold':
            fieldmap_run_list.append('_'.join(row['Filename'].split('_')[1:3]))

    # save out the final fieldmap run list
    fieldmap_dict[new_fieldmap_run_num] = fieldmap_run_list
    return fieldmap_dict

# ...

def main(data_dir):
    # get all imaging data sidecar files
    prw = stat.S_IWRITE | stat.S_IREAD
    layout = BIDSLayout(data_dir)
    json_files = layout.get(datatype=['anat', 'fmap', 'func'], extension='json')
    for json_file in json_files:
        # load the sidecar into a dictionary
        prop = json_file.get_dict()

        # remove the offending fields
        fix_dict(prop)

        # write a fixed version
        os.chmod(json_file.path, prw)
        with open(json_file.path, 'w') as f:
            json.dump(prop, f, indent=4)

    # add IntendedFor field to fieldmaps
    for subject in layout.get_subjects():
        fmappings = get_fieldmap_mapping(data_dir, subject)
        id = 0
        for fmap_run, func_runs in fmappings.items():
            func_files = [
                f'func/sub-{subject}_{func_run}_bold.nii.gz'
                for func_run in func_runs
                ]
            sbref_files = [
                f'func/sub-{subject}_{func_run}_sbref.nii.gz'
                for func_run in func_runs
                ]
            fmap_files = layout.get(
                datatype='fmap', extension='json', subject=subject, run=fmap_run
            )
            
            for fmap_file in fmap_files:
                prop = fmap_file.get_dict()
                prop['IntendedFor'] = func_files + sbref_files
                prop['B0FieldIdentifier'] = f'00000{id}'
                os.chmod(fmap_file.path, prw)
                with open(fmap_file.path, 'w') as f:
                    json.dump(prop, f, indent=4)
            id += 1

    # sort the participants file
    participants_file = os.path.join(data_dir, 'participants.tsv')
    df = pd.read_csv(participants_file, sep='\t')
    df = df.sort_values('participant_id')
    df.to_csv(participants_file, sep='\t', index=False, na_rep='n/a')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='path to BIDS dataset')
    args = parser.parse_args()
    main(args.data_dir)

