#!/bin/bash

# Current time used for file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines the directory where the input files are stored
config_dir="/data/$(whoami)/TRUTH3_StaticDir/"

# Sets up the environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Appends time before Derivation_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log


# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -m /data:/data -r "asetup Athena,24.0.53,here && \
  Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT_el9_batch.root --outputDAODFile=TRUTH3.root --formats TRUTH3 2>&1 | tee pipe_file.log"

# Appends time after Derivation_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Defines the output directory
output_dir="/data/$(whoami)/benchmarks/$curr_time/TRUTH3_el9_container"

# Creates the output directory
mkdir -p ${output_dir}

# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du DAOD_TRUTH3.TRUTH3.root >> split.log

# Moves the log file to the output directory
mv log.Derivation ${output_dir}
mv split.log ${output_dir}
mv pipe_file.log ${output_dir}
