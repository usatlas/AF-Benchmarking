#!/bin/bash

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="${GITHUB_WORKSPACE}/EVNT/EVNTFiles/100xxx/100001"

max_events=10000

# Sets up our working environment
echo "::group::setupATLAS"
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh
echo "::endgroup::"

# Appends time before Gen_tf.py to log file
date +'%H:%H:%S' >> split.log

# Sets up the Ath* version
asetup AthGeneration,23.6.34,here
Gen_tf.py --ecmEnergy=13000.0 --jobConfig="${config_dir}"  --outputEVNTFile=EVNT.root --maxEvents="${max_events}" --randomSeed="${seed}" 2>&1 | tee pipe_file.log

# Appends time after Gen_tf.py to a log file
{
  date +'%H:%M:%S'
  hostname
  du EVNT.root
} >> split.log
