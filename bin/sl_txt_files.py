#!/usr/bin/env python
#
#


import pandas as pd
import argparse


def main(sub):
    beta_dir = f'/corral-repl/utexas/prestonlab/whiterabbit_temp/sub-{sub}/betaseries/'
    imagine_dir = '/corral-repl/utexas/prestonlab/whiterabbit_temp/imagine_tsvs'

    all_runs = []

    for run in [1, 2, 3, 4]:
        events = pd.read_csv(
            f'{imagine_dir}/sub-{sub}_task-imagine_run-0{run}_events.tsv',
            sep='\t'
        )

        df_run = events[['run', 'quartet', 'context_int', 'trial']]
        all_runs.append(df_run)

    df_all = pd.concat(all_runs, ignore_index=True)

    df_all.to_csv(
        f'{beta_dir}/sub-wr261_sl_meta.txt',
        sep='\t', header=False, index=False)

    # take edge trials only
    df_14 = df_all[((df_all['trial'] - 1) % 4 == 0) | (df_all['trial'] % 4 == 0)]

    df_14.to_csv(
        f'{beta_dir}/sub-wr261_sl_meta_1v4.txt',
        sep='\t', header=False, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sub", help="subject number e.g. wr001")
    args = parser.parse_args()
    main(args.sub)
