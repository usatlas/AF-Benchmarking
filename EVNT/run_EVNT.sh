#!/bin/bash

# Simple help menu for the user
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
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -b -c ${1} -r "asetup AthGeneration,23.6.34,here && \
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${2}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${3}"
}

# Takes in the following parameters:
## 1 -- config_dir
## 2 -- Seed
Batch(){
  export atlas_local_root_base=/cvmfs/atlas.cern.ch/repo/atlaslocalrootbase
  source ${atlas_local_root_base}/user/atlaslocalsetup.sh
  asetup athgeneration,23.6.34,here
  Gen_tf.py --ecmenergy=13000.0 --jobconfig=${1}  --outputevntfile=evnt.root --maxevents=10000 --randomseed=${2}
}


main() {
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  # The seed used in the job
  seed=1001

  # Checks for the home directory
  if [[ -d /sdf ]]; then
    local  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT"
    local  config_dir=""
    local  OScontainer="el9"
  elif [[ -d /usatlas ]]
  then
    local  output_dir="/usatlas/workarea/$USER/benchmarks/$curr_time/EVNT"
    local  config_dir="/srv/EVNTFiles/100xxx/100001"
    local  OScontainer="el9"
  elif [[ -d /data ]]
  then
    local  output_dir="/data/selbor/benchmarks/$curr_date/EVNT/"
    local  config_dir="$PWD/100xxx/100001"
    local  OScontainer="centos 7"
  fi

  while [[ "${#}" -gt 0 ]]; do
    case "${1}" in 
      -c|--container)
        Container ${OScontainer} ${config_dir} ${seed}
        mkdir -p ${output_dir}
        mv log.* ${output_dir}
        mv *.generate ${output_dir}
        mv evnt.* ${output_dir}
        exit
        ;;
      -b|--batch)
        Batch ${config_dir} ${seed}
        mkdir -p ${output_dir}
        mv log.* ${output_dir}
        mv *.generate ${output_dir}
        mv evnt.* ${output_dir}
        exit
        ;;
    esac
  done
}

main "${@:-}"


