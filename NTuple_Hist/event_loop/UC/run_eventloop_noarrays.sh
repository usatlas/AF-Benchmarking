#!/bin/bash

# Time that will be used to store the log file
curr_time=$(date +"%Y.%m.%dT%H")

# Setting up
setup ATLAS

# Setting up root
export ALRB_rootVersion=6.34.04-x86_64-el9-gcc13-opt
lsetup root

# Getting start date
date >> eventloop_noarrays.log


# Running the script
python3 ~/AF-Benchmarking/event_loop/UC/event_loop_noarrays.py 2>&1 | tee eventloop_noarrays.log 

# Getting end date
date >> eventloop_noarrays.log

# Getting host name
hostname >> eventloop_noarrays.log


# Output Dir
output_dir="/data/$USER/benchmarks/$curr_time/eventloop_noarrays/"

mkdir -p ${output_dir}

mv eventloop_noarrays.log ${output_dir}
