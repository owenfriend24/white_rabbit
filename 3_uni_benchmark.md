# benchmark analyses:
## Planned Analyses
### 1. source correct vs. incorrect
* 1st level
  *  ev1: correct, ev2: incorrect, ev3: other
  *  contrast 1: correct=1, incorrect=-1, other=0

### 2. boundary sensitivity for different vs same context
* 1st level
  * ev1: same context item 1; ev2: same context item 2, ev3: same context item 3, ev4: same context item4
  * ev5: diff context item 1; ev6: diff context item 2, ev7: diff context item3, ev8: diff context item4
  * ev9: other (no items)
  * Contrast 1: different over same boundary, 4 vs. 1
    * ev1: -2, ev4: -1, ev5: 1, ev8: 2, others: 0
  * Contrast 2: different over same boundary, 3 vs. 2
    * ev2: -2, ev3: -1, ev6: 1, ev7: 2, others: 0
  * Contrast 3: different over same boundary, 43 vs. 21
    * ev1,2: -2, ev3,4: -1, ev5,6: 1, ev7,8: 2, ev9: 0
   
### 3. close vs far in time responses
* 1st level
  * ev1: any_far; ev2: any_far, ev3: other
  * Contrast 1:  close over far
    * ev1: -1, ev2: 1
  * Contrast 2: far over close
    * ev1: 1, ev2: -1

### 4. repetition suppression in same vs. different contexts
* 1st level
 * same ev's #2, will want to extract parameter estimates from each ev in hippocampus and plot

```
wr_univ.py /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/ all wr200
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/source_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/tempdist_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/boundary_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
```
## Running first level analyses
### 1. Generate formatted .txt files for feat
 * .txt files will be outputted into func/univ_txt_files (to keep in consistent directory with events files)
 * confounds - reformats fmriprep output to remove NaN's, movement in each direction and derivatives
 * behavioral data - onset, duration, weight; one .txt file for each Explanatory Variable (varies by analysis)
  * file_types = motion, boundary, source, tempdist, all 
```
wr_univ.py $SCRATCH/wr/new_prepro/derivatives/fmriprep/ <file_type> <subject>
```
example:
```
wr_univ.py $SCRATCH/wr/new_prepro/derivatives/fmriprep/ all wr200
```
### 2. Create template .fsf files using Feat gui (add details here later)
* remote desktop
```
sbatch /share/doc/slurm/job.dcv
touch dcvserver.out ; tail -f dcvserver.out
```
* open feat gui
```
Feat &
```
* create .fsf file and save, download and open as text file to make final edits; see templates in ___ for reference
  
### 3. Generate fsf files for each analysis type
* generates .fsf files for each analysis by editing templates in wr/bin/templates for each subject
* creates univ directory within participant's derivatives folder, with boundary, source, and tempdist subdirectories
 * .fsf files for each analyses stored within respective subdirectory
* boundary:
```
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/boundary_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
```
* source:
```
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/source_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
```
* tempdist
```
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/tempdist_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
```

### 4. Batch run all first level analyses
* will run a first level univariate analyses for each analysis type, for each run, for each subject
* outputted to subject/univ/analysis_type directory within derivatives
```
run_bench_l1.sh $SCRATCH/wr/new_prepro/derivatives/fmriprep wr200
```
example:
```
subs=201:202:203
slaunch -J batch_uni "run_bench_l1.sh $SCRATCH/wr/new_prepro/derivatives/fmriprep {}" $subs -N 1 -n 3 -r 08:00:00 -p normal
```


from Omer - 
Hey, figured out how to keep them in T1. To keep them in T1, instead of moving an MNI or the subject's T1w image into the lower level feat reg folder (before running the higher level analysis), you'll need to move the mean_func.nii.gz image found in the feat folder into the reg directory (and move the identity matrix into the reg folder also like you have before). The lab previously used each subject's T1w image to do so, but that was resulting in some weird transformations into a completely different space.
* rename to standard.nii.gz, you don't need a highres in the reg folder
* rename identity matrix to example_func2standard.mat

```
prep_second.sh $HOME/analysis/wr/bin/templates/2ndlevel_source_3run_template.fsf $FM/sub-wr202/univ wr202 $FM
```
* note - will need a new tmeplate for a 4 run source, and will need to go into each fsf and edit so it aligns properly to the runs where we have both correct and incorrect source memory responses
