#!/bin/bash

# Input/large files should be stored in the /data/$USER directory
# Change <username> to your username
inputFile_dir="/data/<username>/TRUTH3_Native_input_file/"

# Creates the file directory
mkdir -p ${inputFile_dir}

# Moves input files to the input file directory
cp ~/AF-Benchmarking/TRUTH3/EVNT.root ${inputFile_dir}

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${inputFile_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Obtains and appends the host machine to the log file
hostname >> log.Derivation

