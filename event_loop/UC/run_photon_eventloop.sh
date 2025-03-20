#!/bin/bash

# Time that will be used to store the log file
curr_time=$(date +"%Y.%m.%dT%H")

# Setting up
setup ATLAS

# Setting up root
export ALRB_rootVersion=6.34.04-x86_64-el9-gcc13-opt
lsetup root

# Getting start date
date >> photon_eventloop.log

# Running the script
python3 ~/AF-Benchmarking/event_loop/UC/photon_ABCD_eventloop.py 2>&1 | tee photon_eventloop.log 

# Getting end date
date >> photon_eventloop.log

# Getting host name
hostname >> photon_eventloop.log

mv photon_eventloop.log /data/$USER/benchmarks/$curr_time/photon_eventloop/
