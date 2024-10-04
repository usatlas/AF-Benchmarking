#!/bin/bash

if [[ ${1} == c ]]
then
  # Location of input files
  config_dir="EVNTFiles/100xxx/100001/"
  # OS used in the container
  OScontainer="centos7"
  # The seed used in the job
  seed=1001
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthGeneration,23.6.31,here && \
    Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}"
      # Current time used for log file storage
      curr_time=$(date +"%Y.%m.%dT%H")
      output_dir="/sdf/scratch/users/s/selbor/benchmarks/$curr_time/EVNT_container_centos"
      mkdir -p ${output_dir}
      hostname >> log.generate
      du EVNT.root >> log.generate
      mv log.generate ${output_dir}
elif [[ ${1} == e ]]
then
  # UChicago uses the AthGeneration,23.6.34
  OS_container="el9"
  # The seed used in the job
  seed=1001
  # Directory storing the input files
  config_dir="EVNTFiles/100xxx/100001/"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -r "asetup AthGeneration,23.6.34,here && \
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}"
    # Current time used for log file storage
    curr_time=$(date +"%Y.%m.%dT%H")
    output_dir="/sdf/scratch/users/s/selbor/benchmarks/$curr_time/EVNT_container_el/"
    mkdir -p ${output_dir}
    hostname >> log.generate
    du EVNT.root >> log.generate
    mv log.generate ${output_dir}
fi


