#!/bin/bash

# Defining the OS wanted in the container
OS_container="el9"

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="/data/selbor/evnt_el9/100xxx/100001"

# Setting up the working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -m /data:/data -r "asetup AthGeneration,23.6.34,here && \
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}"
  
# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines and makes the output directory
output_dir="/data/selbor/benchmarks/$curr_time/EVNT_contained_el9/"
mkdir -p ${output_dir}

# Obtains and appends the host name and payload size to the log file
hostname >> log.generate
du EVNT.root >> log.generate

# Moves the log file to the output directory
mv log.generate ${output_dir}