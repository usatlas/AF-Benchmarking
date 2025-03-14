#!/bin/bash

curr_time=$(date +"%Y.%m.%dT%H")

# Run this in a container

cd /pscratch/sd/s/selbor/ntuple/coffea

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase


$date >> coffea_hist.log

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "lsetup 'python 3.9.21-x86_64-centos7' &&\

  python3 ~/AF-Benchmarking/NTuple_Hist/coffea/NERSC/example.py 2>&1 | tee coffea_hist.log
"

$date >> coffea_hist.log

hostname >> coffea_hist.log

du ntuple_cfw.pdf >> coffea_hist.log

rm ntuple_cfw.pdf

log_file_dir="/global/homes/s/selbor/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${log_file_dir}

mv coffea_hist.log ${log_file_dir}

