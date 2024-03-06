### Cleaning source behavioral data
1. Download from server - source: PrestonLab/Experiments/Data/WhiteRabbit/scan_data/completed ; dest: Documents/wr_local/behav
2. clean raw data
   ```
   cd Documents/wr_local/analysis
   python clean_raw_behav.py SUB
   ```
   e.g.,
   ```
   python clean_raw_behav.py 200
   ```
3. upload to TACC into subject's func directory
