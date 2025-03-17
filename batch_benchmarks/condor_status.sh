#!/bin/bash


# Time of running this script
curr_date_hour=$(date +"%Y.%m.%dT%H")

# Gets the date.Hour.minute
curr_hour_min=$(date +"%Y.%m.%dT%H.%M")

# File Name
first_file_name="memory_log_${curr_hour_min}.log"
second_file_name="condor_log_${curr_hour_min}.log"

# Getting information from condor
condor_status -compact 2>&1 | tee ${first_file_name}
condor_q -global 2>&1 | tee ${second_file_name}

# Output dir
output_dir="/data/$USER/batch_benchmarks/${curr_date_hour}"

mkdir -p ${output_dir}

# Moves the log file to the benchmarks directory
mv ${first_file_name} ${second_file_name} ${output_dir}
