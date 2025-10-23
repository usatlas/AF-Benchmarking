#!/bin/bash

# The seed used in the job
seed=1001


# Sets up our working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh

# Sets up the Ath* version
asetup AthGeneration,23.6.34,here

# Appends time before Gen_tf.py to log file
date +'%H:%H:%S' >> split.log

Gen_tf.py --ecmEnergy=13000.0 --jobConfig=/atlasgpfs01/usatlas/data/jroblesgo/EVNTJob/native/EVNTFiles/100xxx/100001/  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed} 2>&1 | tee pipe_file.log

# Appends time after Gen_tf.py to log file
date +'%H:%H:%S' >> split.log

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Output directory
output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/${curr_time}/EVNT_native_batch"

# Creates the output directory
mkdir -p "${output_dir}"
# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du EVNT.root >> split.log
# Moves the log file to the output directory
mv log.generate "${output_dir}"
mv split.log "${output_dir}"
mv pipe_file.log "${output_dir}"

# Checks the directory, if it matches it cleans it for the next job
if [ "$(pwd)" = "/atlasgpfs01/usatlas/scratch/jroblesgo/EVNT/native" ]; then
  rm -r ./*
fi
