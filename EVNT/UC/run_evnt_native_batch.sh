#!/bin/bash

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="/data/$(whoami)/evnt/100xxx/100001"

# Sets up our working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Appends time before Gen_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

# Sets up the Ath* version
asetup AthGeneration,23.6.34,here
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed} 2>&1 | tee pipe_file.log

# Appends time before Gen_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Directory where all the output files will be sent to
output_dir="/data/$(whoami)/benchmarks/${curr_time}/EVNT/"

# Makes the output directory
mkdir -p ${output_dir}

# Appends the hostname and payload size to the log files
hostname >> split.log
du EVNT.root >> split.log

# Moves the log file to the output directory
mv log.generate ${output_dir}
mv split.log ${output_dir}
mv pipe_file.log ${output_dir}
