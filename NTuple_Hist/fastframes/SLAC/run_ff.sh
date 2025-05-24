#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

asetup StatAnalysis,0.5.0

cat $HOME/pass.txt | voms-proxy-init -voms atlas

cd /sdf/data/atlas/u/selbor/TutorialClass/build

source setup.sh

cd /sdf/scratch/atlas/selbor/Ntuple_Hist/fastframes/

python3 /sdf/data/atlas/u/selbor/FastFrames/python/FastFrames.py -c /sdf/data/atlas/u/selbor/input_ff/example_config.yml 2>&1 | tee ff.log
