#!/bin/bash

# Config Dir Needed
config_dir="TRUTH3Files/centos/"

# Sets up the ATLAS Environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "asetup AthDerivation,21.2.178.0,here && \
  Reco_tf.py --inputEVNTFile ${config_dir}EVNT_centos.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3"

# current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# There is a madgraph error; I can just raise a flag and have the process skip that step.
output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/TRUTH3_centos7_batch"
mkdir -p ${output_dir}
hostname >> log.EVNTtoDAOD
du TRUTH3.root >> log.EVNTtoDAOD
# Moves the log file to the output directory
mv log.EVNTtoDAOD ${output_dir}
