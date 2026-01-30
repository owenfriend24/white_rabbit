## Remote desktop via TACC
```
sbatch /share/doc/slurm/job.dcv
touch dcvserver.out ; tail -f dcvserver.out
```
* job needs to be running before touch command works
* to quit job:
```
  scancel JOBID
```
* use '&' to open software within session
```
fsleyes &
```
* Ctrl + c in terminal to get back to normal TACC after running job commands

## Plotting motion using fmriprep confound files
* fmriprep outputs some plot but I don't like their formatting, this script gives better ones including reports of mean, sd, and %/# over threshold for FD and DVARS
* .png graphs are outputted to derivatives/motion/sub-{subject}/; use virtual desktop or download via CyberDuck to view 
```
 wr_plot_motion.py <fmriprep directory> <subject>
 ```
example:
```
wr_plot_motion.py $SCRATCH/wr/new_prepro/derivatives/fmriprep wr200
```
