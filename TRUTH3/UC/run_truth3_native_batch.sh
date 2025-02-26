#!/bin/bash

# Input files are stored here
config_dir="/data/$(whoami)/TRUTH3_StaticDir/"

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Appends time before Derivation_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Appends time after Derivation_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines the output directory
output_dir="/data/$(whoami)/benchmarks/$curr_time/TRUTH3"

# Creates the output directory
mkdir -p ${output_dir}

# Obtains and appends the host machine and payload size to the log file
hostname >> split.log
du DAOD_TRUTH3.TRUTH3.root >> split.log

# Moves the log file to the output directory
mv log.Derivation ${output_dir}
mv split.log ${output_dir}
