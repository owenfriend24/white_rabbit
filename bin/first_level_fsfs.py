#!/usr/bin/env python
#
# edit template .fsf file for other subjects and runs

from pathlib import Path
import os
import argparse


def edit_fsf_file(template, out_path, sub, run, num_vols):
    # Read the content of the original .fsf file
    with open(template, 'r') as f:
        fsf_content = f.read()

        
    # Replace 'sub-wr200' with whatever subject we're modeling
    fsf_content = fsf_content.replace('sub-wr200', f'sub-{sub}')

    
    
    if num_vols == '222':
        if 'boundary' in template:
            out_file = f'{out_path}/boundary/sub-{sub}-boundary_second_level.fsf'
        elif 'tempdist' in template:
            out_file = f'{out_path}/tempdist/sub-{sub}-tempdist_second_level.fsf'
        elif 'source' in template:
            out_file = f'{out_path}/source/sub-{sub}-source_second_level.fsf'
    else:
        # Replace 'run-01' with whatever run we're modeling
        fsf_content = fsf_content.replace('run-01', f'run-0{run}')
        fsf_content = fsf_content.replace('run-1', f'run-{run}')
    
        fsf_content = fsf_content.replace('NUM_VOLS', num_vols)
    
        fsf_content = fsf_content.replace('OUT_RUN', f'out_run{run}')
        if  'boundary' in template:  
            out_file = f'{out_path}/boundary/sub-{sub}-boundary_run-0{run}.fsf'
        elif 'source' in template:
            out_file = f'{out_path}/source/sub-{sub}-source_run-0{run}.fsf'
        elif 'tempdist' in template:
            out_file = f'{out_path}/tempdist/sub-{sub}-tempdist_run-0{run}.fsf'
    os.makedirs(os.path.dirname(out_file), exist_ok=True)   
    # Write the modified content to the new .fsf file
    with open(out_file, 'w') as f:
        f.write(fsf_content)

        
def main(template, out_path, sub, run_num, num_vols):
    edit_fsf_file(template, out_path, sub, run_num, num_vols)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("template", help="path to template .fsf file")
    parser.add_argument("out_path", help="output dir (e.g. .../sub-temple001/univ")
    parser.add_argument("sub", help="subject number e.g. temple001")
    parser.add_argument("run_num", help="run to generate .fsf file for")
    parser.add_argument("num_vols", help="number of functional volumes")
    args = parser.parse_args()
    main(args.template, args.out_path, args.sub, args.run_num, args.num_vols)
