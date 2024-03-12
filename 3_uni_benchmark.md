## benchmark analyses:
### Planned Analyses
1. source correct vs. incorrect
* 1st level
  *  ev1: correct, ev2: incorrect, ev3: other
  *  contrast 1: correct=1, incorrect=-1, other=0

2. boundary sensitivity for different vs same context
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
   
3. close vs far in time responses
* 1st level
  * ev1: very far; ev2: far, ev3: close, ev4: very close, ev5: other (no items)
  * Contrast 1: very close over very far, 4 vs. 1
    * ev1: -1, ev4: 1
  * Contrast 2: close over far
    * ev1: -1, ev2: -1, ev3: 1, ev4: 1, others: 0
  * Contrast 3: very far over very close
    * ev1: 1, ev4: -1
  * Contrast 4: far over close

4. repetition suppression in same vs. different contexts
* 1st level
 * same ev's #2, will want to extract parameter estimates from each ev in hippocampus and plot

```
wr_univ.py /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/ all wr200
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/source_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/tempdist_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/boundary_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
```
### Running first level analyses
1. Generate formatted .txt files for feat
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
2. Create template .fsf files using Feat gui (add details here later)
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
  
4. Generate fsf files for each analysis type
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

4. Batch run all first level analyses
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
