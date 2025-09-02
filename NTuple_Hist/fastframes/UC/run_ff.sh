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

cp ~/AF-Benchmarking/NTuple_Hist/fastframes/UC/mc20e_example_config.yml ${working_dir}

# Sets up ATLAS environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -m /data/ -r "asetup StatAnalysis,0.6.3 &&\
  lsetup emi &&\
  cat /data/selbor/pass/pass.txt | voms-proxy-init -voms atlas &&\
  source /data/selbor/FastFramesTutorial/TutorialClass/build/setup.sh &&\
  cd - &&\
  lsetup 'python 3.9.22-x86_64-el9' &&\
  pip3 install pyyaml &&\
  date >> split.log &&\
  python3 /srv/FastFramesTutorial/FastFrames/python/FastFrames.py -c ${working_dir}/mc20e_example_config.yml 2>&1 | tee ff.log"

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
