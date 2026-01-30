# Pre-Processing of fMRI Data
## 1. Source white rabbit profile
* sets paths to bin, activates 'tempenv' virutal environment (same as temple)
* can also enter 'wr' as shortcut; will turn terminal purple to show WR is the active profile
```
source $HOME/analysis/wr/wr_profile
wr
```
* Code is currently in my home/analysis/wr/bin directory and sourcing the profile in home/analysis/wr adds those scripts to Path. Can help set up on other machines
## 2. Convert source DICOM data to BIDS formatting
* Raw data from scanner will label ppt as wr_### (e.g., wr_200)
  * heudiconv does not allow special characters like underscores, so will update to wr200 once in BIDS
  * need to remember how to refer to subject based on what level of preprocessing you're at, but otherwise, this is a helpful reminder for where the data is at 
* copy source data from corral to lonestar6
```
cp -R $CORR/wr_200 $WORK/wr/sourcedata

```
* Run heudiconv on source data

  * Make sure the WR scripts are on your Path, set participant variable, then use slaunch to convert. Below code is for one subject at a time and will run on a development node.
Aborted scans should not be passed in, if you have any aborted partial scans delete them or save them elsewhere before running heudiconv
  * wr_backup_heu.sh assigns correct directory structure for scans from the BIC's archive if direct export has issues
```
slaunch -J heudiconv "wr_heudiconv.sh {} <raw data directory> <heuricstic file> <output directory>" <subject> -N 1 -n 1 -r 00:30:00 -p development
```
example:
```
sub=wr_001
slaunch -J heudiconv "wr_heudiconv.sh {} $WORK/wr/sourcedata/ $HOME/analysis/wr/bin/wr_heuristic.py $SCRATCH/wr/new_prepro/" $sub -N 1 -n 1 -r 00:30:00 -p development
```
## 3. Add fieldmap information to functional run .json files
* Need to make sure before that no extraneous/unused fieldmaps remain (e.g., if you had to abort one fieldmap during scanning, that should be removed before running heudiconv).
* Can confirm that fieldmaps are correctly attached by looking at .json files for each fieldmap and looking at 'IntendedFor' field at bottom
* Will assign 'B0FieldIdentifier' in sidecar file as well, important to make sure same ID is assigned to AP and PA fieldmaps of same run
```
wr_bids_post.py <BIDS dataset>
```
example:
```
wr_bids_post.py $SCRATCH/wr/prepro
```

## 4. Run fmriprep on BIDS-formatted data
* runs fmriPrep v23.1.3 via Singularity/Apptainer image in $WORK; Still points to Neal's freesurfer license but might also use freesurfer inside singularity image
* wr_fmriprep.sh includes command line that specifies some parameters including:
  * participant label - passed in with job launch; temple_### denotes raw data, temple### denotes data converted to BIDS (BIDS does not allow underscores)
 * std. dvars threshold = 1.5
 * framewise displacement threshold = 0.5
 * high-pass filter = 128
 * output spaces = fsaverage:den-164k anat:res-native (we'll use custom MNI transformations later on)
 * omp-nthreads = 12
 * num_threads = 18
 * mem_mb = 60000
 * skip_bids_validation (make sure BIDS compliant when running heudiconv)
```
slaunch -J fmriprep "wr_fmriprep.sh <BIDS data> {}" <subject> -N 1 -n 1 -r 08:00:00 -p normal
```
example:
```
sub=wr200
slaunch -J fmriprep "wr_fmriprep.sh $SCRATCH/wr/prepro {}" $sub -N 1 -n 1 -r 08:00:00 -p normal
```
* Like heudiconv, I like to run with slaunch which requires defining the participant before. fMRIPrep needs to run on a compute node and takes about 8 hours
 * WR data gave me problems when running parallel processes on same nodes whereas temple did not; worth looking into later  
* Both T2 images should be automatically used for freesurfer plial surface reconstruction, but only one will be outputted as a preprocessed T2 image. I believe it's averaging between the images passed in but will need to confirm if the pre-processed versions of those images ever need to be used later (freesurfer uses the raw images for reconstruction with the preprocessed T1w image)

## 5. Create functional brainmask with freesurfer parcellations and skullstrip functional data
* takes about 5 minutes on a development node
* brainmask will be outputted in subject's freesurfer directory in mri/out/ as brainmask_func_dilated.nii.gz
 * got dilation from Kate, check on whether we still want that moving forward
* Skullstripped runs will end up in new directory within func; can later on run ________.sh to swap them into func (for BIDS formatting) and put the original preprocessed functional runs (not skullstripped or smoothed) in a separate directory
 * will implement this after WR benchmarks, since current univariate templates are set up to get functional data from this directory 
```
slaunch -J prep_func "prep_func_data.sh <freesurfer directory> <fmriprep directory> {} imagine 4" $sub -N 1 -n 1 -r 01:00:00 -p normal
```
example:
```
sub=wr200
slaunch -J prep_func "prep_func_data.sh $SCRATCH/wr/new_prepro/derivatives/fmriprep/sourcedata/freesurfer $SCRATCH/wr/new_prepro/derivatives/fmriprep {} imagine 4" $sub -N 1 -n 1 -r 01:00:00 -p normal
```
## 6. Skullstrip anatomical image and create transform images/affine files for registration between T1 functional, T1 anatomical, and MNI space
* takes about 15 minutes on development node
* run transformations with skullstripped data
* This script will also create a skullstripped T1 anatomical in both native T1 and MNI space
* should add this to the end of prep_func_data.sh later on so both run as part of same process
```
mni_transforms.sh <fmriprep directory> <subject>
```
example:
```
sub=wr200
slaunch -J mni "mni_transforms.sh $SCRATCH/wr/new_prepro/derivatives/fmriprep {}" $sub -N 1 -n 1 -r 01:00:00 -p normal
```
## 7. Smooth functional data with 4mm kernel
* set to run on and output to data in func/skullstripped_T1 directory (created during step 5). After smoothing, run ____.sh
```
wr_smooth.sh <fmriprep directory> <freesurfer directory> <subject> task
```
example:
```
slaunch -J smooth "wr_smooth.sh $SCRATCH/wr/new_prepro/derivatives/fmriprep $SCRATCH/wr/new_prepro/derivatives/fmriprep/sourcedata/freesurfer {} imagine" $sub -N 1 -n 1 -r 01:00:00 -p normal
```









