#!/bin/bash

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="/data/$USER/evnt/100xxx/100001"

# Sets up our working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets up the Ath* version
asetup AthGeneration,23.6.34,here
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Directory where all the output files will be sent to
output_dir="/data/$USER/benchmarks/${curr_time}/EVNT/"

# Makes the output directory
mkdir -p ${output_dir}

# Appends the host name and the payload size to the log file
hostname >> log.generate
du EVNT.root >> log.generate

# Moves the log file to the output directory
mv log.generate ${output_dir}

