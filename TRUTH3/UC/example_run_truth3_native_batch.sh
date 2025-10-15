#!/bin/bash

# Input/large files should always be stored in the /data/$USER directory
inputFile_dir="/data/$(whoami)/TRUTH3_Native_input_file/"

# Creates the input file directory defined above
mkdir -p ${inputFile_dir}

# Copies the input files to the designated directory
cp ~/AF-Benchmarking/TRUTH3/EVNT.root ${inputFile_dir}

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${inputFile_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Obtains and appends the host machine to the log file
hostname >> log.Derivation
