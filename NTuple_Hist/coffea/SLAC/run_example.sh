#! /bin/bash


# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Working directory
work_dir="/sdf/home/s/selbor/Ntuple_Hist/coffea"

cd ${work_dir}

source /sdf/data/atlas/u/selbor/testing/bin/activate

start_time=$date

$start_time >> coffea_hist.log

python3 /sdf/home/s/selbor/AF-Benchmarking/NTuple_Hist/coffea/SLAC/example.py 2>&1 | tee coffea_hist.log

end_time=$date

$end_time >> coffea_hist.log

hostname >> coffea_hist.log

du ntuple_cfw.pdf >> coffea_hist.log

rm ntuple_cfw.pdf

log_file_dir="/sdf/home/s/selbor/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${log_file_dir}

mv coffea_hist.log ${log_file_dir}
