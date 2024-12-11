#!/bin/bash

# Input files are stored here
config_dir="/data/$USER/TRUTH3_StaticDir/"

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT_interactive.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines the output directory
output_dir="/data/$USER/benchmarks/$curr_time/TRUTH3_interactive"

# Creates the output directory
mkdir -p ${output_dir}

# Obtains and appends the host machine and payload size to the log file
hostname >> log.Derivation
du DAOD_TRUTH3.TRUTH3.root >> log.Derivation

# Moves the log file to the output directory
mv log.Derivation ${output_dir}
