#!/bin/bash

# Time that will be used to store the log file
curr_time=$(date +"%Y.%m.%dT%H")

cd /data/selbor/ntuple_hist/eventloop_noarrays/

# Setting up
setupATLAS

# Setting up root
lsetup "views LCG_107a_ATLAS_2 x86_64-el9-gcc13-opt"


# Getting start date
date >> eventloop_noarrays.log


# Running the script
python3 ~/AF-Benchmarking/NTuple_Hist/event_loop/UC/event_loop_noarrays.py 2>&1 | tee eventloop_noarrays.log 

# Getting end date
date >> eventloop_noarrays.log

# Getting host name
hostname >> eventloop_noarrays.log


# Output Dir
output_dir="/data/$USER/benchmarks/$curr_time/eventloop_noarrays/"

mkdir -p ${output_dir}

mv eventloop_noarrays.log ${output_dir}
