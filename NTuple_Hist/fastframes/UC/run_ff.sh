#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

yml_dir="${GITHUB_WORKSPACE}/NTuple_Hist/fastframes/UC/"

# Sets up our working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh

# Set up for FF
asetup StatAnalysis,0.6.3
lsetup emi
printf "%s" "${VOMS_PASSWORD}" | voms-proxy-init -voms atlas
# shellcheck disable=SC1091
source /data/selbor/FastFramesTutorial/TutorialClass/build/setup.sh

date >> split.log

python3 /data/selbor/FastFramesTutorial/FastFrames/python/FastFrames.py -c "${yml_dir}"mc20e_example_config.yml 2>&1 | tee ff.log

# Getting the date and time after running script
date >> split.log

# Getting the host-machine's name
hostname >> split.log

# Directory that needs to be cleaned
cleanup_dir="/home/selbor/ntuple/ff"

if [[ -d "${cleanup_dir}" && "${cleanup_dir}" == "/home/selbor/ntuple/ff" ]]; then
    rm -rf "${cleanup_dir:?}/"*
fi
