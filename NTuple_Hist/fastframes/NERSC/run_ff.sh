#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

cd /global/cfs/cdirs/m2616/selbor/

# Sets up ATLAS environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -m /global/cfs/cdirs/m2616/selbor/ -c el9 -r "asetup StatAnalysis,0.6.2 &&\
  source /srv/FastFramesTutorial/TutorialClass/build/setup.sh &&\
  python3 /srv/FastFramesTutorial/FastFrames/python/FastFrames.py -c /srv/ff_input/mc20e_example_config.yml 2>&1 | tee ff.log"
hostname >> ff.log

# output directory
output_dir="/global/cfs/cdirs/m2616/selbor/benchmarks/$curr_date/FF_NTuple"

# Creates output dir
mkdir -p ${output_dir}

# Moves log to outputdir
mv ff.log ${output_dir}
