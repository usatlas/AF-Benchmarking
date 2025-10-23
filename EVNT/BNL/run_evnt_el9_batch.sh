#!/bin/bash
# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")


# The OS used in the container
OScontainer="el9"

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -m /atlasgpfs01 -r "asetup AthGeneration,23.6.34,here &&\
  echo $(date +"%Y.%m.%d.%H.%S") >> split.log &&\
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=/atlasgpfs01/usatlas/data/jroblesgo/EVNTJob/el/EVNTFiles/100xxx/100001/  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=1001 2>&1 | tee pipe_file.log &&\
  echo $(date +"%Y.%m.%d.%H.%S") >> split.log"

# Output directory
output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/${curr_time}/EVNT_el9_batch"

# Creates the output directory
mkdir -p "${output_dir}"
# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du EVNT.root >> split.log
# Moves the log file to the output directory
mv log.generate "${output_dir}"
mv split.log "${output_dir}"
mv pipe_file.log "${output_dir}"

# Checks the directory, if it matches it cleans it for the next job
if [ "$(pwd)" = "/atlasgpfs01/usatlas/scratch/jroblesgo/EVNT/el" ]; then
  rm -r ./*
fi
