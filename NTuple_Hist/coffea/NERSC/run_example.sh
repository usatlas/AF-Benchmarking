#!/bin/bash

curr_time=$(date +"%Y.%m.%dT%H")

# Run this in a container

cd /pscratch/sd/s/selbor/ntuple/coffea

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase


$date >> split.log

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -r "lsetup 'python 3.9.22-x86_64-el9' &&\
  pip3 install  light_roast-0.1.dev10+ge21defc-py3-none-any.whl &&\
  pip3 install atlas_schema &&\

  python3 ~/AF-Benchmarking/NTuple_Hist/coffea/NERSC/example.py 2>&1 | tee coffea_hist.log"

$date >> split.log

hostname >> split.log

log_file_dir="/global/cfs/cdirs/m2616/selbor/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${log_file_dir}

mv coffea_hist.log ${log_file_dir}
mv split.log ${log_file_dir}
