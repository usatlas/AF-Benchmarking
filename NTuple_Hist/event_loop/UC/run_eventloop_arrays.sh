#!/bin/bash

# Time that will be used to store the log file
curr_time=$(date +"%Y.%m.%dT%H")

cd /data/selbor/ntuple_hist/eventloop_arrays/

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
lsetup "views LCG_107a_ATLAS_2 x86_64-el9-gcc13-opt"

# Getting start date
date >> split.log

# Running the script
python3 ~/AF-Benchmarking/NTuple_Hist/event_loop/UC/event_loop_arrays.py 2>&1 | tee eventloop_arrays.log 

# Getting end date
date >> split.log

# Getting host name
hostname >> split.log

# Output Dir
output_dir="/data/${whoami}/benchmarks/$curr_time/eventloop_arrays/"

mkdir -p ${output_dir}

mv eventloop_arrays.log ${output_dir}
mv split.log ${output_dir}
