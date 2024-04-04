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
 * same ev's #2, extract parameter estimates from each ev in hippocampus (and subregion ROI's and plot to compare same vs. different contexts

# Executing analyses:
## 1st level analyses.
### 2. Reformat behavioral data to .txt files with format \[onset duration weight] and no headers
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
### 3. Create template files using Feat gui via remote desktop
* see above for design parameters
### 4. Create .fsf files based on templates to run first level analyses for all subjects and runs
* will create subdirectories within sub/univ for each analysis
```
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/source_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/tempdist_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/boundary_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
```
### 4. Batch run all first level analyses
* will run a first level univariate analyses for each analysis type, for each run, for each subject
* outputted to subject/univ/analysis_type directory within derivatives
* analyses will fail if there is not behavior to model (i.e., if participant got 0 incorrect responses on source memory for 1 run). This isn't an issue with running the rest of the first level analyses, but will need to be accounted for in the 2nd level
```
run_bench_l1.sh $SCRATCH/wr/new_prepro/derivatives/fmriprep wr200
```
example:
```
subs=201:202:203
slaunch -J batch_uni "run_bench_l1.sh $SCRATCH/wr/new_prepro/derivatives/fmriprep {}" $subs -N 1 -n 3 -r 08:00:00 -p normal
```
## 2nd level analyses
### 1. Create fsf files for each second level analysis based on 2nd level templates, also copy mean_func.nii.gz from feat output into reg folder with identity matrix to ensure no transformation out of T1w participant space
* for source memory, there is a three run and 4 run source memory template (in case ppt's get all source questions correct in a given run). 3 run template automatically omits the fourth run, but can be easily adjusted on a subject by subject basis
```
prep_second.sh $HOME/analysis/wr/bin/templates/2ndlevel_boundary_template.fsf $FM/sub-wr202/univ wr202 $FM
prep_second.sh $HOME/analysis/wr/bin/templates/2ndlevel_tempdist_template.fsf $FM/sub-wr202/univ wr202 $FM
prep_second.sh $HOME/analysis/wr/bin/templates/2ndlevel_source_4run_template.fsf $FM/sub-wr202/univ wr202 $FM
prep_second.sh $HOME/analysis/wr/bin/templates/2ndlevel_source_3run_template.fsf $FM/sub-wr202/univ wr202 $FM
```
### 2. Run all second level analyses
```
run_bench_seconds.sh subject fmriprep_dir
```

## Repetition Suppression Analysis
### 1. create bilateral hippocampus mask in functional space from freesurfer output
```
fs_hpc.sh wr204
```

### 2. transform MNI hippocampus and subfield masks into participant T1w functional space, extract parameter estimates for each EV in each run within each mask
```
rep_sup.py $FM wr204
```
### 3. download all_pe.csv files for each ppt and plot

