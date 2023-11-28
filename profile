#!/bin/bash

#script directory

# study name and directory
export STUDY=temple
export SRCDIR=$HOME/analysis/whiterabbit
export STUDYDIR=$STOCKYARD2/ls6/whiterabbit
export BATCHDIR=$STOCKYARD2/ls6/whiterabbit/batch/launchscripts

# add analysis scripts to path
export PATH=$PATH:$SRCDIR/bin
export STUDYDIR=$STOCKYARD2/ls6/whiterabbit
. $STOCKYARD2/ls6/wr_env/bin/activate

# subjects
export SUBJNOS=000
export SUBIDS=000
export BIDIDS=000
