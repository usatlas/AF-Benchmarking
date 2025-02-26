#!/bin/bash

# Defines the directory where the input files are stored
config_dir="/data/$USER/TRUTH3_StaticDir/"

# Defines the OS the container will have
OScontainer="el9"

# Sets up the working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Appends time before Derivation_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -m /data:/data -r "asetup Athena,24.0.53,here && \
  Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT_el9_interactive.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

# Appends time after Derivation_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Current time used for file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines the output directory
output_dir="/data/$USER/benchmarks/$curr_time/TRUTH3_el9_container_interactive"

# Creates the output directory
mkdir -p ${output_dir}

# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du DAOD_TRUTH3.TRUTH3.root >> split.log

# Moves the log file to the output directory
mv log.Derivation ${output_dir}
mv split.log ${output_dir}
