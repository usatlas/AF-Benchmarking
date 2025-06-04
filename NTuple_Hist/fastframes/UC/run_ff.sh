#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

working_dir="/data/selbor/ntuple/fastframes/"


# Goes into the job directory if it exits, creates it otherwise
if [ -d ${working_dir} ]; then
  cd ${working_dir}
else
  mkdir -p ${working_dir}
  cd ${working_dir}
fi

# Sets up ATLAS environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -m /data/ -r "asetup StatAnalysis,0.5.0 &&\
  lsetup emi &&\
  cat $HOME/pass.txt | voms-proxy-init -voms atlas &&\
  cd /data/$(whoami)/ntuple_hist/TutorialClass/build &&\
  source setup.sh &&\
  cd - &&\
  lsetup 'python 3.9.22-x86_64-el9' &&\
  pip3 install pyyaml &&\
  date >> split.log &&\
  python3 /data/$(whoami)/ntuple_hist/FastFrames/python/FastFrames.py -c /data/$(whoami)/input/example_config.yml 2>&1 | tee ff.log"

# Getting the date and time after running script
date >> split.log

# Getting the host-machine's name
hostname >> split.log

# output directory
output_dir="/data/$(whoami)/benchmarks/${curr_date}/FF_NTuple"

# Creates output dir
mkdir -p ${output_dir}

# Moves log to outputdir
mv ff.log ${output_dir}
mv split.log ${output_dir}
