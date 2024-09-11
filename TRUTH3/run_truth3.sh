#!/bin/bash

### NTS for now the input dir is fine, but in the future change it so that all three jobs aren't fighting for the same input files. ###

# Takes the following parameters:
## 1 -- The container OS the job will be using
## 2 -- The input dir for the input files
Container(){
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${1} -r "asetup Athena,24.0.53,here && \
    Derivation_tf.py --CA True --inputEVNTFile ${2}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"
}

# Takes the following parameters:
## 1 -- input_dir; where the input files are located
Batch(){
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  asetup Athena,24.0.53,here
  Derivation_tf.py --CA True --inputEVNTFile ${1}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3
}

main() {
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  # The seed used in the job
  seed=1001

  # Checks for the home directory
  if [[ -d /sdf ]]; then
    local  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/TRUTH3"
    local  config_dir=$HOME/evntFiles/100xxx/100001
    local  OScontainer="centos7"
    Container ${OScontainer} ${config_dir} ${seed}
  elif [[ -d /usatlas ]]
  then
    # There is a madgraph error; I can just raise a flag and have the process skip that step.
    local  output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/TRUTH3"
    local  config_dir="EVNTFiles/100xxx/100001/"
    local  OScontainer="el9"
    cd /usatlas/workarea/jroblesgo
    Container ${OScontainer} ${config_dir} ${seed}
  elif [[ -d /data ]]
  then
    local  output_dir="/data/selbor/benchmarks/$curr_date/TRUTH3/"
    local  config_dir="/data/selbor/evnt/100xxx/100001/"
    local  OScontainer="centos7"
    Batch ${config_dir} ${seed}
  fi
  mkdir -p ${output_dir}
  mv myjob.* ${output_dir}
  mv log.* ${output_dir}
  
  #hostname >> ${output_dir}/log.*
  # I still need to get the payload size into the log file.
}

# Call the main function
main

