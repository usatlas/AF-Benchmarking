#!/bin/bash

# Simple help menu
Help() {
cat << EOF
  ${0} [-c|--container] [-b|--batch]
  CONTAINER -- The container the user wants to use.
  BATCH -- The batch system is used to run the job
EOF
}

# Takes in the following parameters:
## 1 -- Container wanted
## 2 -- config_dir
## 3 -- Seed
Container(){
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${1} -r "asetup AthGeneration,23.6.31,here ; pwd && \
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${2}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${3}"
}

# Takes in the following parameters:
## 1 -- config_dir
## 2 -- Seed
Batch(){
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  asetup AthGeneration,23.6.31,here
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${1}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${2}
}


main() {
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  # The seed used in the job
  seed=1001

  # Checks for the home directory
  if [[ -d /sdf ]]; then
    local  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT"
    local  config_dir="$HOME/evntFiles/100xxx/100001"
    local  OScontainer="centos7"
    Container ${OScontainer} ${config_dir} ${seed}
  elif [[ -d /usatlas ]]
  then
    local  output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/EVNT"
    # I need to change the config_dir to be in scratch:
    ## Have it check for the existence of /EVNTFiles/
    ## If it exists proceed
    ## If it doesn't, then copy it from the home directory to the config_dir
    local  config_dir="/atlasgpfs01/usatlas/data/$USER/EVNTFiles/100xxx/100001/"
    local  OScontainer="centos7"
    Batch ${config_dir} ${seed}
  elif [[ -d /data ]]
  then
    local  output_dir="/data/selbor/benchmarks/$curr_date/EVNT/"
    local  config_dir="/data/selbor/evnt/100xxx/100001/"
    local  OScontainer="centos7"
    Batch ${config_dir} ${seed}
  fi
  mkdir -p ${output_dir}
  mv log.* ${output_dir}
  mv *.generate ${output_dir}
  mv evnt.* ${output_dir}
}

# Call the main function
main


