#!/bin/bash


# Time of running this script
curr_date_hour=$(date +"%Y.%m.%dT%H")

# Getting information from condor
condor_status -compact 2>&1 | tee condor_log_${curr_date_hour}.log

# Moves the log file to the benchmarks directory
mv condor_log_${curr_date_hour}.log /data/selbor/benchmarks/${curr_date_hour}/condor_info
