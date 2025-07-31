#!/bin/bash

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="/sdf/data/atlas/u/selbor/EVNTJob/container_el/EVNTFiles/100xxx/100001/"

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

user_name=$USER
first_letter=${user_name:0:1}

cp -r /sdf/home/$first_letter/$USER/AF-Benchmarking/EVNT/EVNTFiles .

# Appends time before Gen_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

asetup AthGeneration,23.6.34,here
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir} --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed} 2>&1 | tee pipe_file.log

# Appends time after Gen_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du EVNT.root >> split.log
