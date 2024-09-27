#!/bin/bash


if [[ ${1} == n ]]
then
  config_dir="TRUTH3Files/"
  OScontainer="el9"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup Athena,24.0.53,here && \
    Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/TRUTH3"
  mkdir -p ${output_dir}
  hostname >> log.generate
  du DAOD_TRUTH3.TRUTH3.root >> log.generate
fi

