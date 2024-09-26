#!/bin/bash

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

output_dir="/data/selbor/benchmarks/$curr_date/TRUTH3/"

config_dir="/data/selbor/TRUTH3_StaticDir/"

if [[ ${1} == n ]]
then 
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  asetup Athena,24.0.53,here
  Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3
elif [[ ${1} == c ]]
then
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -m /data:/data - r " asetup Athena,24.0.53,here && \
    Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"
fi

mkdir -p ${output_dir}
hostname >> log.generate
du DAOD_TRUTH3.TRUTH3.root >> log.generate
mv myjob.* ${output_dir}
mv log.generate ${output_dir}

