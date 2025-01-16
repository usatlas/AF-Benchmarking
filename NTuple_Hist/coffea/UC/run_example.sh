#! /bin/bash


# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Working directory
work_dir="$DATA/ntuple_hist/coffea_fw/"

cd ${work_dir}

source ../bin/activate

python3 example.py 2>&1 | coffea_hist.log

log_file_dir="$DATA/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${log_file_dir}

mv coffea_hist.log ${log_file_dir}
