#!/bin/bash

# Native OS for UC is CentOS7
if [[ ${1} == n ]]
then
    # The seed used in the job
  seed=1001

  # Directory storing the input files
  config_dir="/data/selbor/evnt/100xxx/100001"

  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  asetup AthGeneration,23.6.34,here
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  # Directory where all the output files will be sent to
  output_dir="/data/selbor/benchmarks/${curr_time}/EVNT/"

  mkdir -p ${output_dir}
  hostname >> log.generate
  du EVNT.root >> log.generate
  mv log.generate ${output_dir}
  mv myjob.* ${output_dir}
elif [[ ${1} == e ]]
then
  # UChicago uses the AthGeneration,23.6.34
  OS_container="el9"

  # The seed used in the job
  seed=1001

  # Directory storing the input files
  config_dir="/data/selbor/evnt_el9/100xxx/100001"

  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OS_container} -m /data:/data -r "asetup AthGeneration,23.6.34,here && \
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}"
  
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/EVNT_contained_el9/"
  mkdir -p ${output_dir}
  hostname >> log.generate
  du EVNT.root >> log.generate
  mv log.generate ${output_dir}
  mv myjob.* ${output_dir}
elif [[ ${1} == c ]]
then
  # UChicago uses the AthGeneration,23.6.34
  OS_container="centos7"

  # The seed used in the job
  seed=1001

  # Directory storing the input files
  config_dir="/data/selbor/evnt_centos/100xxx/100001"

  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthGeneration,23.6.31,here && \
    Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}" 
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  output_dir="/data/selbor/benchmarks/$curr_time/EVNT_contained_centos7/"
  mkdir -p ${output_dir}
  hostname >> log.generate
  du EVNT.root >> log.generate
  mv log.generate ${output_dir}
  mv myjob.* ${output_dir}
fi
