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
    Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}"
      # Current time used for log file storage
      curr_time=$(date +"%Y.%m.%dT%H")
      output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT_container_centos"
elif [[ ${1} == e ]]
then
  # UChicago uses the AthGeneration,23.6.34
  OS_container="el9"
  # The seed used in the job
  seed=1001
  # Directory storing the input files
  config_dir="EVNTFile/100xxx/100001/"
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -m /data:/data -r "asetup AthGeneration,23.6.34,here && \
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}"
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/EVNT_container_el/"

fi

mkdir -p ${output_dir}
hostname >> log.generate
du EVNT.root >> log.generate
mv log.generate ${output_dir}
mv myjob.* ${output_dir}

