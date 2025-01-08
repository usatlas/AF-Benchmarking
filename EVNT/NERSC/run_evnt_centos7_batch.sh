#!/bin/bash
  
OS_container="centos7"

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="evnt_centos7/100xxx/100001"
cp -r $HOME/evnt_centos7/ .
# Creates the ATLAS Environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -r "asetup AthGeneration,23.6.31,here && \
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}"

rm -r evnt_centos/
