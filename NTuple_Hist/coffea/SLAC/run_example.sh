#!/bin/bash

# # Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Working directory
work_dir="/sdf/scratch/users/s/selbor/coffea_testing"

cd ${work_dir}

date >> split.log

# Setting up environment and container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

export ALRB_localConfigDir=$HOME/localConfig

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -m /sdf/data/atlas/ -r "python3 example.py 2>&1 | tee coffea_hist.log"


date >> split.log

hostname >> split.log

log_file_dir="/sdf/home/s/selbor/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${log_file_dir}

mv coffea_hist.log ${log_file_dir}
mv split.log ${log_file_dir}
