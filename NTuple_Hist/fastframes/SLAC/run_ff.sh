#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

echo "Start of Script"

echo "Current dir"

pwd 

asetup StatAnalysis,0.5.0 

cd /srv/TutorialClass/build

echo "Changed dir"

pwd

ls

source setup.sh

cd -

python3 /sdf/data/atlas/u/selbor/FastFrames/python/FastFrames.py -c /sdf/data/atlas/u/selbor/input_ff/example_config.yml 2>&1 | tee ff.log

mv ff.log $HOME
