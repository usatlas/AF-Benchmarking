#!/bin/bash

# Run this in a container

curr_time=$(date +"%Y.%m.%dT%H")

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/coffea

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "lsetup 'python 3.9.21-x86_64-centos7' &&\
  pwd $(date +"%Y.%m.%d.%H.%S") >> split.log &&\
  python3 ~/AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py 2>&1 | tee coffea_hist.log &&\
  pwd $(date +"%Y.%m.%d.%H.%S") >> split.log"

hostname >> split.log


output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${output_dir}

mv coffea_hist.log ${output_dir}
mv split.log ${output_dir}

