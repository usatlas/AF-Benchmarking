#!/bin/bash


config_dir="/data/selbor/evnt/100xxx/100001/"

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

output_dir="/data/selbor/benchmarks/$curr_date/TRUTH3/"
mkdir -p ${output_dir}
mv myjob.* ${output_dir}
mv log.* ${output_dir}
 
