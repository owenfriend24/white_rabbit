# White Rabbit Pre-Processing of fMRI Data
## 1. Source white rabbit profile
* sets paths to bin, activates 'tempenv' virutal environment (same as temple)
```
source $HOME/analysis/wr/wr_profile
```
* Code is currently in my home/analysis/wr/bin directory and sourcing the profile in home/analysis/wr adds those scripts to Path. Can help set up on other machines
## 2. Convert source DICOM data to BIDS formatting
* Raw data from scanner will label ppt as wr_### (e.g., wr_200)
  * heudiconv does not allow special characters like underscores, so will update to wr200 once in BIDS
  * need to remember how to refer to subject based on what level of preprocessing you're at, but otherwise, this is a helpful reminder for where the data is at 
* copy source data from corral to lonestar6
```
scp -R /corral/utexas/prestonlab/whiterabbit_temp/wr_200 $WORK/wr/sourcedata
```
* Run heudiconv on source data

  * Make sure the WR scripts are on your Path, set participant variable, then use slaunch to convert. Below code is for one subject at a time and will run on a development node.
Aborted scans should not be passed in, if you have any aborted partial scans delete them or save them elsewhere before running heudiconv
```
slaunch -J heudiconv "wr_heudiconv.sh {} <raw data directory> <heuricstic file> <output directory>" <subject> -N 1 -n 1 -r 00:30:00 -p development
```
example:
```
sub=wr_001
slaunch -J heudiconv "wr_heudiconv.sh {} $WORK/wr/sourcedata/ $HOME/analysis/wr/bin/wr_heuristic.py $SCRATCH/wr/prepro/" $sub -N 1 -n 1 -r 00:30:00 -p development
```
