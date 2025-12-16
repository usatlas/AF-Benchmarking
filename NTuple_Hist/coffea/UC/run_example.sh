#!/bin/bash

# Gets the current time

curr_time=$(date +"%Y.%m.%dT%H")

date >> split.log

#cp ${GITHUB_WORKSPACE}/NTuple_Hist/coffea/UC/example.py .
#cp ${GITHUB_WORKSPACE}/NTuple_Hist/coffea/light_roast-0.1.dev10+ge21defc-py3-none-any.whl .

# Setting up environment and container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir="$HOME"/localConfig
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh -c el9 -m /data -r "lsetup 'python 3.9.22-x86_64-el9' &&\
  pip3 install ${GITHUB_WORKSPACE}/NTuple_Hist/coffea/light_roast-0.1.dev10+ge21defc-py3-none-any.whl &&\
  pip3 install atlas_schema &&\
python3.9 ${GITHUB_WORKSPACE}/NTuple_Hist/coffea/UC/example.py  2>&1 | tee coffea_hist.log"

date >> split.log

hostname >> split.log

# Directory that needs to be cleaned
cleanup_dir="/home/selbor/ntuple/coffea"

if [[ -d "${cleanup_dir}" && "${cleanup_dir}" == "/home/selbor/ntuple/coffea" ]]; then
    rm -rf "${cleanup_dir:?}/"*
fi
