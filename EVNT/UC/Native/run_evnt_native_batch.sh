#!/bin/bash

curr_time=$(date +"%Y.%m.%dT%H")

# The seed used in the job
seed=1001

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"

jo="${repo_root}/EVNTFiles/100xxx/100001/MC100001_MGPy8EG_A14N23LO_MET_25_N2_100_N1_80_WB.py"

ls "${jo}"

# Sets up our working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh

# Appends time before Gen_tf.py to log file
date +'%H:%H:%S' >> split.log

# Sets up the Ath* version
asetup AthGeneration,23.6.34,here
Gen_tf.py --ecmEnergy=13000.0 --jobConfig="${jo}"  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed="${seed}" 2>&1 | tee pipe_file.log

# Appends time before Gen_tf.py to a log file
date +'%H:%H:%S' >> split.log

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Directory where all the output files will be sent to
output_dir="/home/$(whoami)/benchmarks/${curr_time}/EVNT/"

# Makes the output directory
mkdir -p "${output_dir}"

# Appends the hostname and payload size to the log files
hostname >> split.log
du EVNT.root >> split.log

# Moves the log file to the output directory
mv log.generate "${output_dir}"
mv split.log "${output_dir}"
mv pipe_file.log "${output_dir}"
mv evnt_native.* "${output_dir}"

# Directory that needs to be cleaned
cleanup_dir="/home/selbor/EVNTJob/native"

if [[ -d "${cleanup_dir}" && "${cleanup_dir}" == "/home/selbor/EVNTJob/native" ]]; then
    rm -rf "${cleanup_dir:?}/"*
fi
