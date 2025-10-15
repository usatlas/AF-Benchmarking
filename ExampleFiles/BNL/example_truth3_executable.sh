#!/bin/bash

# Config Dir Needed
config_dir="TRUTH3Files/"

# Sets up the environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh -c el9 -r "asetup Athena,24.0.53,here && \
  Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT_el9_batch.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

# Obtains and appends the host name to the log file
hostname >> log.Derivation
