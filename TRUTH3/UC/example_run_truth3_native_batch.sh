#!/bin/bash

# Input files are stored here
input_file_dir="$HOME/AF-Benchmarking/TRUTH3/"

# Where we want the job to execute from
job_dir="$DATA/TRUTH3_native"

# Makes the directory we want the job to execute from
mkdir -p ${job_dir}

# Goes into the desired directory
cd ${job_dir}

# Copies the input files to the desired directory
cp ${config_dir}/EVNT.root .

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here

# Initiates process with input file EVNT.root and output TRUTH3.root
Derivation_tf.py --CA True --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

