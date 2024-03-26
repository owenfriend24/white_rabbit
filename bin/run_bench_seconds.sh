#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: run_bench_seconds.sh subject fmriprep_dir"
    exit 1
fi

subject=$1
fm_dir=$2


# Load any necessary modules
module load python3/3.9.7

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/wr/wr_profile

# Move to the directory containing your Python script
cd /home1/09123/ofriend/analysis/wr/bin


feat "$fm_dir/sub-$subject/univ/boundary/sub-$subject-boundary_second_level.fsf"
feat "$fm_dir/sub-$subject/univ/source/sub-$subject-source_second_level.fsf"
feat "$fm_dir/sub-$subject/univ/tempdist/sub-$subject-tempdist_second_level.fsf"
