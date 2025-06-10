#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

asetup StatAnalysis,0.5.0

cd /sdf/data/atlas/u/selbor/TutorialClass/build

source setup.sh

cd -

python3 /srv/FastFramesTutorial/FastFrames/python/FastFrames.py -c /sdf/data/atlas/u/selbor/input_ff/example_config.yml 2>&1 | tee ff.log

mv ff.log /srv/benchmarks/${curr_date}/FF_Hist/

