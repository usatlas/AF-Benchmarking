#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

asetup StatAnalysis,0.6.2

cd /sdf/data/atlas/u/selbor/FastFramesTutorial/TutorialClass/build

source setup.sh

cd -

python3 /srv/FastFramesTutorial/FastFrames/python/FastFrames.py -c /sdf/data/atlas/u/selbor/input_ff/mc20e_example_config.yml 2>&1 | tee ff.log

file_dir="/sdf/data/atlas/u/selbor/benchmarks/${curr_date}/FF_Hist/"

mkdir -p ${file_dir}

mv ff.log ${file_dir}

