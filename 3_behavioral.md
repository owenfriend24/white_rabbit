## clean behavioral data for use in neuroimaging analyses
### 1. Download from server - source: PrestonLab/Experiments/Data/WhiteRabbit/scan_data/completed ; dest: Documents/wr_local/behav/WhiteRabbit_###
### 2. Clean raw data
```
cd Documents/wr_local/analysis
python clean_raw_behav.py <subject>
```
no 'wr' for sub, e.g.,
```
python clean_raw_behav.py 200
```
* will output to Documents/wr_local/behav/cleaned/sub-wr###_clean-events directory
### 3. upload events files to TACC into subject's derivatives/sub-/func directory via Cyberduck
