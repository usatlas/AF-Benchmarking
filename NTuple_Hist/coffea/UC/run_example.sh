#! /bin/bash


# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Working directory
work_dir="/data/$(whoami)/ntuple_hist/coffea_fw/"

cd ${work_dir}

source ../bin/activate


$date >> split.log

python3 example.py 2>&1 | tee coffea_hist.log

$date >> split.log


hostname >> split.log

log_file_dir="/data/$(whoami)/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${log_file_dir}

mv coffea_hist.log ${log_file_dir}
mv split.log ${log_file_dir}
