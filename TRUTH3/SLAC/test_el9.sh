#!/bin/bash

cp -r /home/$USER/TRUTH3Files/ . 
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile /srv/TRUTH3Files/el9/EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Defines the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Defines the output directory where the log file will be stored
output_dir="/home/$USER/benchmarks/${curr_time}/TRUTH3_el9_container"

# Creates the output directory
mkdir -p ${output_dir}
# Appends the host-name to the end of the log file
hostname >> log.Derivation
# Appends the size of the output DAOD file to the end of the log file
du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
# Moves the log file to the output directory defined above
mv log.Derivation ${output_dir}
