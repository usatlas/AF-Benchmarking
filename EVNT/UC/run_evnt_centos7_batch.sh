#!/bin/bash
  
OS_container="centos7"

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="/data/selbor/evnt_centos/100xxx/100001"

# Creates the ATLAS Environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -m /data:/data -r "asetup AthGeneration,23.6.31,here && \
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}"

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines and makes the output directory
output_dir="/data/selbor/benchmarks/$curr_time/EVNT_contained_centos7/"
mkdir -p ${output_dir}

# Appends the hostname and payload size to the log files
hostname >> log.generate
du EVNT.root >> log.generate

# Moves the log file to the output directory
mv log.generate ${output_dir}
