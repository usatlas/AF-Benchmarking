#!/bin/bash

# Gets the current time

curr_time=$(date +"%Y.%m.%dT%H")

# Defining the directory the job will be running in
working_dir="/data/$(whoami)/ntuple/coffea/"

# Goes into the job directory if it exits, creates it otherwise
if [ -d "${working_dir}" ]; then
  cd "${working_dir}" || exit
else
  mkdir -p "${working_dir}"
  cd "${working_dir}" || exit
fi

date >> split.log

cp /home/"$(whoami)"/AF-Benchmarking/NTuple_Hist/coffea/UC/example.py .
cp /home/"$(whoami)"/AF-Benchmarking/NTuple_Hist/coffea/light_roast-0.1.dev10+ge21defc-py3-none-any.whl .

# Setting up environment and container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir="$HOME"/localConfig
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh -c el9 -m /data/ -r "lsetup 'python 3.9.22-x86_64-el9' &&\
pip3 install  light_roast-0.1.dev10+ge21defc-py3-none-any.whl &&\
pip3 install atlas_schema &&\
python3.9 example.py  2>&1 | tee coffea_hist.log"

date >> split.log

hostname >> split.log

log_file_dir="/data/$(whoami)/benchmarks/${curr_time}/Coffea_Hist/"

mkdir -p "${log_file_dir}"

mv coffea_hist.log "${log_file_dir}"
mv split.log "${log_file_dir}"
