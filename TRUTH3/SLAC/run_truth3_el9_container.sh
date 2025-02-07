#!/bin/bash

cp -r /sdf/data/atlas/u/$USER/TRUTH3Job/container_el/EVNT.root .
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Defines the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Defines the output directory where the log file will be stored
output_dir="/sdf/data/atlas/u/$USER/benchmarks/${curr_time}/TRUTH3_el9_container"

# Creates the output directory
mkdir -p ${output_dir}
# Appends the host-name to the end of the log file
hostname >> log.Derivation
# Appends the size of the output DAOD file to the end of the log file
du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
# Moves the log file to the output directory defined above
mv log.Derivation ${output_dir}
