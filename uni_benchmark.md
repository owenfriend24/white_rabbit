### benchmark analyses:
source correct vs. incorrect
* running 1st level now,
  *  ev1: correct, ev2: incorrect, ev3: other
  *  contrast 1: correct=1, incorrect=-1, other=0

boundary sensitivity for different vs same context
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
   
close vs far in time responses
* 1st level
  * ev1: very far; ev2: far, ev3: close, ev4: very close, ev5: other (no items)
  * Contrast 1: very close over very far, 4 vs. 1
    * ev1: -1, ev4: 1
  * Contrast 2: close over far
    * ev1: -1, ev2: -1, ev3: 1, ev4: 1, others: 0
  * Contrast 3: very far over very close
    * ev1: 1, ev4: -1
  * Contrast 4: far over close


```
wr_univ.py /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/ all wr200
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/source_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/tempdist_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
first_level_fsfs.sh $HOME/analysis/wr/bin/templates/boundary_template.fsf /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/sub-wr200/univ wr200 /scratch/09123/ofriend/wr/new_prepro/derivatives/fmriprep/
```