#!/bin/bash

# Time that will be used to store the log file
curr_time=$(date +"%Y.%m.%dT%H")

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/event_loop/

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -m /atlasgpfs01/usatlas/data/ -r "export ALRB_rootVersion=6.34.04-x86_64-el9-gcc13-opt
  lsetup root
  date >> photon_eventloop.log
  python3 ~/AF-Benchmarking/event_loop/BNL/photon_ABCD_eventloop.py 2>&1 | tee photon_eventloop.log"

# Getting end date
date >> photon_eventloop.log

# Getting host name
hostname >> photon_eventloop.log

output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/photon_eventloop/"

mkdir -p ${output_dir}

mv photon_eventloop.log ${output_dir}
