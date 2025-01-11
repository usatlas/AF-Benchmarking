#/bin/bash

# Input files are stored here
input_file_dir="$HOME/AF-Benchmarking/TRUTH3/"

# Copies the input files to the desired directory
cp ${input_file_dir}/EVNT.root .

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here

# Initiates process with input file EVNT.root and output TRUTH3.root
Derivation_tf.py --CA True --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Obtains and appends the host machine to the log file
hostname >> log.Derivation
