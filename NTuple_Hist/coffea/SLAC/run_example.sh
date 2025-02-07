#! /bin/bash


# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Working directory
work_dir="/sdf/data/atlas/u/selbor/Ntuple_Hist/coffea"

cd ${work_dir}

start_time=$date

$start_time >> coffea_hist.log

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "lsetup 'python 3.9.21-x86_64-centos7' &&\

  python3 ./AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py
"

end_time=$date

$end_time >> coffea_hist.log

hostname >> coffea_hist.log

du ntuple_cfw.pdf >> coffea_hist.log

rm ntuple_cfw.pdf

log_file_dir="/sdf/data/atlas/u/selbor/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p ${log_file_dir}

mv coffea_hist.log ${log_file_dir}
