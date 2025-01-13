#!/bin/bash

# Input files are stored here
# Input/large files should always be stored in the /data/$USER directory
inputFile_dir="/data/$(whoami)/TRUTH3_Native_input_file/"

mkdir -p ${config_dir}

cp ~/AF-Benchmarking/TRUTH3/EVNT.root ${config_dir}

job_dir="/data/$(whoami)/TRUTH3_Native_example"

mkdir -p ${job_dir}

cd ${job_dir}


# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Obtains and appends the host machine and payload size to the log file
hostname >> log.Derivation

