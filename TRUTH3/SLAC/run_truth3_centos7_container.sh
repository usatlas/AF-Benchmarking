#!/bin/bash


username=$USER
first_letter=${username:0:1}

cp -r /sdf/home/$first_letter/$USER/AF-Benchmarking/TRUTH3/EVNT.root .


asetup AthDerivation,21.2.178.0,here
Reco_tf.py --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3

# Defines the current time
curr_time=$(date +"%Y.%m.%dT%H")
# Defines the output directory where the log file will be stored
output_dir="/sdf/home/$first_letter/$USER/benchmarks/${curr_time}/TRUTH3_centos7_container"
# Creates the output directory
mkdir -p ${output_dir}
# Appends the host-name to the end of the log file
hostname >> log.EVNTtoDAOD
# Appends the size of the output DAOD file to the end of the log file
du DAOD_TRUTH3.TRUTH3.root >> log.EVNTtoDAOD
# Moves the log file to the output directory defined above
mv log.EVNTtoDAOD ${output_dir}
