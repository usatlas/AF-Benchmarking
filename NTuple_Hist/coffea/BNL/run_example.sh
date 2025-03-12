#!/bin/bash

# Run this in a container

cd /atlasgpfs01/usatlas/data/jroblesgo/ntuple_coffea_job

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "lsetup 'python 3.9.21-x86_64-centos7' &&\
  pwd $(date +"%Y.%m.%d.%H.%S") >> coffea_hist.log &&\
  python3 ~/AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py 2>&1 | tee coffea_hist.log &&\
  pwd $(date +"%Y.%m.%d.%H.%S") >> coffea_hist.log"

hostname >> coffea_hist.log

curr_time=$(date +"%Y.%m.%dT%H")

output_dir="/usatlas/u/jroblesgo/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${output_dir}

mv coffea_hist.log ${output_dir}

if [ $(pwd)="/atlasgpfs01/usatlas/data/jroblesgo/ntuple_coffea_job" ]; then
  rm ntuple_cfw.pdf
fi
