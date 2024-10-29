#!/bin/bash


curr_time=$(date +"%Y.%m.%dT%H")

config_dir="/home/selbor/TRUTH3Files/centos7_interactive/"
OScontainer="centos7"
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthDerivation,21.2.178.0,here && \
  Reco_tf.py --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3"


output_dir="/home/selbor/benchmarks/$curr_time/TRUTH3_centos7_container_interactive"
mkdir -p ${output_dir}
hostname >> log.EVNTtoDAOD
du DAOD_TRUTH3.TRUTH3.root >> log.EVNTtoDAOD
mv log.EVNTtoDAOD ${output_dir}
