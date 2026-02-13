#!/bin/bash

### set up experiment info ###
#expdir='/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep'
expdir='/corral-repl/utexas/prestonlab/whiterabbit_temp/'
sub=$1

betadir=${expdir}/sub-${sub}/betaseries

#match
fslmerge -t ${betadir}/run1_items.nii.gz ${betadir}/betaOUT_run-1*
fslmerge -t ${betadir}/run2_items.nii.gz ${betadir}/betaOUT_run-2*
fslmerge -t ${betadir}/run3_items.nii.gz ${betadir}/betaOUT_run-3*
fslmerge -t ${betadir}/run4_items.nii.gz ${betadir}/betaOUT_run-4*

# remove intermediate files to maintain space on corral
rm ${betadir}/betaOUT_run-*
