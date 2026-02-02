#!/bin/bash

# Ensure at least one argument (subject) is provided
if [[ $# -lt 1 ]]; then
    echo "Usage: batch_betaseries.sh subject [drop_run=N]"
    exit 1
fi

### Set up experiment info ###
expdir='/corral-repl/utexas/prestonlab/whiterabbit_temp'
sub=$1
drop_run=""

# Check for optional drop_run argument
for arg in "$@"; do
    if [[ $arg == drop_run=* ]]; then
        drop_run="${arg#drop_run=}"
    fi
done

# Load environment
source /home1/09123/ofriend/analysis/white_rabbit/wr_profile

# Run preprocessing steps
/home1/09123/ofriend/analysis/white_rabbit/bin/prep_imagine.py $expdir both $sub
/home1/09123/ofriend/analysis/white_rabbit/bin/sl_txt_files.py $sub
/home1/09123/ofriend/analysis/white_rabbit/bin/beta_fsfs.sh $sub
/home1/09123/ofriend/analysis/white_rabbit/bin/beta_files.sh $sub

# keeping here for now for batch running
/home1/09123/ofriend/analysis/white_rabbit/bin/create_hip_masks.sh $sub $CORR
/home1/09123/ofriend/analysis/white_rabbit/bin/create_gm_mask.sh $sub

# Setup betaseries directory
betadir=$expdir/sub-${sub}/betaseries
mkdir -p "$betadir"
cd "$betadir"

# Activate Python environment
#source /home1/09123/ofriend/analysis/white_rabbit/rsa_env/bin/activate
/home1/09123/ofriend/analysis/white_rabbit/bin/betaseries_est.py $sub

# Run appropriate merge script based on drop_run flag
if [[ -n $drop_run ]]; then
    echo "Dropping run $drop_run. Running merge_betas_drop1.sh..."
    /home1/09123/ofriend/analysis/white_rabbit/bin/merge_betas_drop1.sh $sub $drop_run
else
    echo "No run drop specified. Running merge_betas_byrun.sh..."
    /home1/09123/ofriend/analysis/white_rabbit/bin/merge_betas_byrun.sh $sub
fi

fslmerge -t ${betadir}/all_items.nii.gz ${betadir}/run1_items.nii.gz ${betadir}/run2_items.nii.gz ${betadir}/run3_items.nii.gz ${betadir}/run4_items.nii.gz

fslselectvols -i ${betadir}/all_items.nii.gz -o ${betadir}/1v4_items.nii.gz --vols=/home1/09123/ofriend/analysis/white_rabbit/templates/vols.txt

