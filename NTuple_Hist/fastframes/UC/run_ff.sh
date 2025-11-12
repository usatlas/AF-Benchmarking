#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

working_dir="/home/selbor/ntuple/ff/"


# Goes into the job directory if it exits, creates it otherwise
if [ -d "${working_dir}" ]; then
  cd "${working_dir}" || exit
else
  mkdir -p "${working_dir}"
  cd "${working_dir}" || exit
fi

cp ~/AF-Benchmarking/NTuple_Hist/fastframes/UC/mc20e_example_config.yml ${working_dir}

# Sets up our working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh

# Set up for FF
asetup StatAnalysis,0.6.3
lsetup emi
cat /data/selbor/pass/pass.txt | voms-proxy-init -voms atlas
# shellcheck disable=SC1091
source /data/selbor/FastFramesTutorial/TutorialClass/build/setup.sh

date >> split.log

python3 /data/selbor/FastFramesTutorial/FastFrames/python/FastFrames.py -c ${working_dir}/mc20e_example_config.yml 2>&1 | tee ff.log

# Getting the date and time after running script
date >> split.log

# Getting the host-machine's name
hostname >> split.log

# output directory
output_dir="/home/$(whoami)/benchmarks/${curr_date}/FF_NTuple"

# Creates output dir
mkdir -p "${output_dir}"

# Moves log to outputdir
mv ff.log "${output_dir}"
mv split.log "${output_dir}"

# Directory that needs to be cleaned
cleanup_dir="/home/selbor/ntuple/ff"

if [[ -d "${cleanup_dir}" && "${cleanup_dir}" == "/home/selbor/ntuple/ff" ]]; then
    rm -rf "${cleanup_dir:?}/"*
fi
