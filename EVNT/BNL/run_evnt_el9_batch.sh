#!/bin/bash


# The OS used in the container
OScontainer="el9"

# Copying input files to working directory
cp -r ~/AF-Benchmarking/EVNT/EVNTFiles .

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthGeneration,23.6.34,here &&\
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=EVNTFiles/100xxx/100001/  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=1001"

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Output directory
output_dir="/atlasgpfs01/usatlas/data/$USER/benchmarks/$curr_time/EVNT_el9_batch"

# Creates the output directory
mkdir -p ${output_dir}
# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du EVNT.root >> split.log
# Moves the log file to the output directory
mv log.generate ${output_dir}
mv split.log ${output_dir}
