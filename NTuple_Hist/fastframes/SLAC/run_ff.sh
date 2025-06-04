#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

echo "Start of Script"

echo "Current dir"

pwd 

asetup StatAnalysis,0.5.0 >> command_out.txt

cd /sdf/data/atlas/u/selbor/TutorialClass/build

pwd >> command_out.txt

source setup.sh >> command_out.txt

cd - >> command_out.txt

python3 /sdf/data/atlas/u/selbor/FastFrames/python/FastFrames.py -c /sdf/data/atlas/u/selbor/input_ff/example_config.yml 2>&1 | tee ff.log

mv ff.log $HOME

mv command_out.txt $HOME
