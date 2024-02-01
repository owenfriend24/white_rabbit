## Preprocessing White Rabbit Neuroimaging Data from Prisma ##

### Participant Naming Convention ###
Participant numbers (including participant ID enterred when registering participant on scanner) should follow convention 'wr_###' (e.g., wr_001, wr_210, etc.). 
When converting dicoms to BIDS format using heudiconv, this will automatically be renamed to wr### (e.g., sub-wr001, sub-wr210, etc.) because heudiconv doesn't accept underscores.
I still like to use the underscore for the raw data so it's immediately obvious when looking at a directory whether that data has been converted or not.

### WR Scan Data Location ###
First test scan was uploaded to corral/utexas/prestonlab/prisma_testing/, need to figure out permanent storage place. Trying to pre-process directly from corral caused a weird permissions
issue for me that I didn't really dive into but copying into my work directory worked fine

### WR Code ###
Code is currently in my home/analysis/wr/bin directory and sourcing the profile in home/analysis/wr adds those scripts to Path. Can help set up on other machines
```
source $HOME/analysis/wr/wr_profile
```
### Running Heudiconv ###
Make sure the WR scripts are on your Path, set participant variable, then use slaunch to convert. Below code is for one subject at a time and will run on a development node.
Aborted scans should not be passed in, if you have any aborted partial scans delete them or save them elsewhere before running heudiconv
```
slaunch -J heudiconv "wr_heudiconv.sh {} <raw data directory> <heuricstic file> <output directory>" <subject> -N 1 -n 1 -r 00:30:00 -p development
```
example:
```
sub=wr_001
slaunch -J heudiconv "wr_heudiconv.sh {} $WORK/wr/sourcedata/ $HOME/analysis/wr/bin/wr_heuristic.py $SCRATCH/wr/prepro/" $sub -N 1 -n 1 -r 00:30:00 -p development
```

### Adding fieldmap information to functional run .json files ###
Need to make sure before that no extraneous/unused fieldmaps remain (e.g., if you had to abort one fieldmap during scanning, that needs to be removed before running heudiconv).
Can confirm that fieldmaps are correctly attached by looking at .json files for each fieldmap and looking at 'IntendedFor' field at bottom
```
wr_bids_post.py <BIDS dataset>
```
example:
```
wr_bids_post.py $SCRATCH/wr/prepro
```

### Run fmriprep on BIDS data ###
Like heudiconv, I like to run with slaunch which requires defining the participant before. fMRIPrep needs to run on a compute node and takes a super long time.
```
slaunch -J fmriprep "wr_fmriprep.sh <BIDS data> {}" <subject> -N 1 -n 1 -r 08:00:00 -p normal
```
example:
```
sub=wr_001
slaunch -J fmriprep "wr_fmriprep.sh $SCRATCH/wr/prepro {}" $sub -N 1 -n 1 -r 08:00:00 -p normal
```
