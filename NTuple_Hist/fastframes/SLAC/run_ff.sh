#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

asetup StatAnalysis,0.5.0 

cd /srv/TutorialClass/build

pwd

source setup.sh

cd -

python3 /sdf/data/atlas/u/selbor/FastFrames/python/FastFrames.py -c /sdf/data/atlas/u/selbor/input_ff/example_config.yml 2>&1 | tee ff.log

mv ff.log $HOME
