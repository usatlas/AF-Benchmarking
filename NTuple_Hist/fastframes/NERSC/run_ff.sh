#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

ddir

# Sets up ATLAS environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -r "asetup StatAnalysis,0.5.0
  lsetup emi
  cat $HOME/pass.txt | voms-proxy-init -voms atlas
  cd /srv/TutorialClass/build
  source setup.sh
  cd -
  echo date >> ff.log
  python3 /srv/FastFrames/python/FastFrames.py -c $HOME/AF-Benchmarking/NTuple_Hist/fastframes/NERSC/example_config.yml 2>&1 | tee ff.log"
  echo date >> ff.log
  echo hostname >> ff.log

# output directory
output_dir="/global/cfs/cdirs/m2616/selbor/benchmarks/$curr_time/FF_NTuple"

# Creates output dir
mkdir -p ${output_dir}

# Moves log to outputdir
mv ff.log ${output_dir}
