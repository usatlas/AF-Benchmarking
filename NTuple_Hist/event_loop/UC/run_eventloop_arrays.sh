#!/bin/bash

# Time that will be used to store the log file
curr_time=$(date +"%Y.%m.%dT%H")

cd /data/selbor/ntuple_hist/eventloop_arrays/

# Setting up
setup ATLAS

# Setting up root
export ALRB_rootVersion=6.34.04-x86_64-el9-gcc13-opt
lsetup root

# Getting start date
date >> eventloop_arrays.log

# Running the script
python3 ~/AF-Benchmarking/NTuple_Hist/event_loop/UC/event_loop_arrays.py 2>&1 | tee eventloop_arrays.log 

# Getting end date
date >> eventloop_arrays.log

# Getting host name
hostname >> eventloop_arrays.log

# Output Dir
output_dir="/data/$USER/benchmarks/$curr_time/eventloop_arrays/"

mkdir -p ${output_dir}

mv eventloop_arrays.log ${output_dir}
