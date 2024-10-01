#!/bin/bash


if [[ ${1} == n ]]
then
  config_dir="/data/selbor/TRUTH3_StaticDir/"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  asetup Athena,24.0.53,here 
  Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3
  # current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/TRUTH3"
  mkdir -p ${output_dir}
  hostname >> log.Derivation
  du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
  mv myjob.* ${output_dir}
  mv log.Derivation ${output_dir}
elif [[ ${1} == i ]]
then
  config_dir="/data/selbor/TRUTH3_StaticDir/"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -m /data:/data -r "asetup AthDerivation,21.2.178.0,here && \
    Reco_tf.py --inputEVNTFile ${config_dir}EVNT_centos_interactive.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3"
  # current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/TRUTH3_centos_interactive/"
  mkdir -p ${output_dir}
  hostname >> log.Derivation
  du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
  mv log.Derivation ${output_dir}
elif [[ ${1} == c ]]
then
  config_dir="/data/selbor/TRUTH3_StaticDir/"
  
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -m /data:/data -r "AthDerivation,21.2.178.0,here && \
    Reco_tf.py --inputEVNTFile ${config_dir}EVNT_centos_interactive.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3"
  # current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/TRUTH3_centos/"
  mkdir -p ${output_dir}
  hostname >> log.Derivation
  du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
  mv myjob.* ${output_dir}
  mv log.Derivation ${output_dir}
elif [[ ${1} == e ]]
then
  config_dir="/data/selbor/TRUTH3_StaticDir/"
  OScontainer="el9"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -m /data:/data -r "asetup Athena,24.0.53,here && \
    Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT_el9_batch.root --outputDAODFile=TRUTH3.root --formats TRUTH3"
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/TRUTH3_el9_container"
  mkdir -p ${output_dir}
  hostname >> log.Derivation
  du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
elif [[ ${1} == I ]]
then
  config_dir="/data/selbor/TRUTH3_StaticDir/"
  OScontainer="el9"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -m /data:/data -r "asetup Athena,24.0.53,here && \
    Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT_el9_interactive.root --outputDAODFile=TRUTH3.root --formats TRUTH3"
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/TRUTH3_el9_container_interactive"
  mkdir -p ${output_dir}
  hostname >> log.Derivation
  du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
fi

