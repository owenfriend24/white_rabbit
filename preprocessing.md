# Pre-Processing:

## 1. Source relevant profile
* activates virtual environment with relevant packages, sets some paths (will need to be adjusted for each tacc profile)
```
cd $HOME/analysis/whiterabbit
source profile
```

## 2. Convert source DICOM data to BIDS formatting
* add more nodes/jobs if doing more than one sub at once
```
slaunch -J heudiconv "wr_heudiconv.sh {} $WORK/whiterabbit/sourcedata $HOME/analysis/whiterabbit/bin/wr_heuristic.py $SCRATCH/whiterabbit/prepro" $SUBIDS -N 1 -n 1 -r 00:30:00 -p development
```

## 3. Add fieldmap information to BIDS formatted raw data (need to figure out new double fieldmap)

   
## 4. Run fmriprep
* add more nodes/jobs if doing more than one sub at once
```
slaunch -J fmriprep “wr_fmriprep.sh $SCRATCH/temple/prepro {}" $BIDIDS -N 1 -n 1 -r 08:00:00 -p normal
```
