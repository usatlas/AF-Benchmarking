#!/bin/bash

# Defines the current time
curr_time=$(date +"%Y.%m.%dT%H")

username=$USER
first_letter=${username:0:1}

cp -r /sdf/home/$first_letter/$USER/AF-Benchmarking/TRUTH3/EVNT.root .

# Appends time before Derivation_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3 2>&1 | tee pipe_file.log

# Appends time after Derivation_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Defines the output directory where the log file will be stored
output_dir="/sdf/home/$first_letter/$USER/benchmarks/${curr_time}/TRUTH3_el9_container"

# Creates the output directory
mkdir -p ${output_dir}
# Appends the host-name to the end of the log file
hostname >> split.log
# Appends the size of the output DAOD file to the end of the log file
du DAOD_TRUTH3.TRUTH3.root >> split.log
# Moves the log file to the output directory defined above
mv log.Derivation ${output_dir}
mv split.log ${output_dir}
mv pipe_file.log ${output_dir}
