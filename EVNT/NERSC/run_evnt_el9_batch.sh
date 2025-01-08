#!/bin/bash

# Defining the OS wanted in the container
OS_container="el9"

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="evnt_el9/100xxx/100001"
cp -r $HOME/evnt_el9/ .
# Setting up the working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -r "asetup AthGeneration,23.6.34,here && \
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}"

rm -r evnt_el9/
