#!/bin/bash

curr_time=$(date +"%Y.%m.%dT%H")
touch $HOME/truth3.${curr_time}.txt
echo "The script is started" >> $HOME/truth3.${curr_time}.txt
if [[ ${1} == e ]]
then
  config_dir="TRUTH3Files/"
  OScontainer="el9"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  echo "The container is started" >> $HOME/truth3.${curr_time}.txt
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup Athena,24.0.53,here && \
    Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3" 2>&1 | tee $HOME/truth3.${curr_time}.txt
  echo "The container is done" >> $HOME/truth3.${curr_time}.txt
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/sdf/data/atlas/u/selbor/benchmarks/$curr_time/TRUTH3_el9_container"
  mkdir -p ${output_dir}
  hostname >> log.Derivation
  du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
  mv log.Derivation ${output_dir}
elif [[ ${1} == c ]]
then
  config_dir="TRUTH3Files/"
  OScontainer="centos7"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthDerivation,21.2.178.0,here && \
    Reco_tf.py --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3"

  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/TRUTH3_centos7_container"
  mkdir -p ${output_dir}
  hostname >> log.EVNTtoDAOD
  du DAOD_TRUTH3.TRUTH3.root >> log.EVNTtoDAOD
  mv log.EVNTtoDAOD ${output_dir}
fi

