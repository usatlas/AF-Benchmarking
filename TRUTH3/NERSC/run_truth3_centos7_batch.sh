#!/bin/bash


# Defines the OS the container will have
OScontainer="centos7"
cp ~/AF-Benchmarking/TRUTH3/EVNT.root .
# Sets up the working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthDerivation,21.2.178.0,here && \
  Reco_tf.py --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3"

rm EVNT.root

# current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defining the output directory
output_dir="$HOME/benchmarks/$curr_time/TRUTH3_centos/"

# Creates the output directory
mkdir -p ${output_dir}

# Obtains and appends the host name and payload size to the log file
hostname >> log.EVNTtoDAOD
du DAOD_TRUTH3.TRUTH3.root >> log.EVNTtoDAOD

# Moves the log file to the output directory
mv log.EVNTtoDAOD ${output_dir}
