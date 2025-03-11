#!/bin/bash


# The seed used in the job
seed=1001

# Directory where the input files are stored
config_dir="EVNTFiles/100xxx/100001/"

# The OS used in the container
OScontainer="el9"

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "cp -r ~/AF-Benchmarking/EVNT/EVNTFiles . &&\
  asetup AthGeneration,23.6.34,here &&\
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}"

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
