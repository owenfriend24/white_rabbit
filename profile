#!/bin/bash

#script directory

# study name and directory
export STUDY=temple
export SRCDIR=$HOME/analysis/temple
export STUDYDIR=$STOCKYARD2/ls6/temple
export BATCHDIR=$STOCKYARD2/ls6/temple/batch/launchscripts

# add analysis scripts to path
export PATH=$PATH:$SRCDIR/bin
export STUDYDIR=$STOCKYARD2/ls6/temple
. $STOCKYARD2/ls6/tempenv/bin/activate

# subjects
export SUBJNOS=016
export SUBIDS=temple_016
export BIDIDS=temple016
