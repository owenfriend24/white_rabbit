#!/bin/bash

SUBNUM=$1
runNUM="1 2 3 4"

for sbj in $SUBNUM

do


    for run in $runNUM

    do


    feat_model /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run} #fsf file

    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}_cov.png
    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}_cov.ppm
    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}.con
    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}.frf
    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}.min
    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}.png
    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}.ppm
    rm /corral-repl/utexas/prestonlab/whiterabbit_temp/sub-${sbj}/betaseries/sub-${sbj}_betaL1_run-${run}.trg

    done


done
