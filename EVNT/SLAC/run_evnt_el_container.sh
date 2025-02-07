#!/bin/bash

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="EVNTFiles/100xxx/100001/"

# Copies input files dir to the working dir
cp -r /sdf/data/atlas/u/$USER/EVNTFiles/ .

asetup AthGeneration,23.6.34,here
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")
# Defines the output directory
output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT_container_el/"
# Creates the output directory
mkdir -p ${output_dir}
# Obtains and appends the host name and payload size to the log file
hostname >> log.generate
du EVNT.root >> log.generate
# Moves the log file to the output directory
mv log.generate ${output_dir}
