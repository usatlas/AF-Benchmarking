#!/bin/bash

echo "::group::setupATLAS"
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh
echo "::endgroup::"
lsetup "views LCG_107a_ATLAS_2 x86_64-el9-gcc13-opt"


# Getting start date
date >> split.log


# Running the script
python3 "${GITHUB_WORKSPACE}"/NTuple_Hist/event_loop/UC/standard/event_loop_noarrays.py 2>&1 | tee eventloop_noarrays.log

# Getting end date
date >> split.log

# Getting host name
hostname >> split.log
