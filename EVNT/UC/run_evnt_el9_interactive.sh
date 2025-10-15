#!/bin/bash

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defining the OS wanted in the container
OS_container="el9"

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="/data/$(whoami)/evnt_el9/100xxx/100001"

# Setting up the working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Appends time before Gen_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -m /data:/data -r "asetup AthGeneration,23.6.34,here && \
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed} 2>&1 | tee pipe_file.log"

# Appends time after Gen_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du EVNT.root >> split.log
