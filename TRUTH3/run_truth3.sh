#!/bin/bash
curr_date=$(date +"%Y.%m.%dT%H")

# NTS: The input dir is just the input files; similar to the ones the EVNT Job requires

# This same block works at SLAC
# But it doesn't seem to run at BNL
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
asetup Athena,24.0.53,here

Derivation_tf.py --CA True --inputEVNTFile ${inputdir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

main() {
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  # The seed used in the job
  seed=1001

  # Checks for the home directory
  if [[ -d /sdf ]]; then
    local  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT"
    local  config_dir=$HOME/evntFiles/100xxx/100001
    local  OScontainer="centos7"
    Container ${OScontainer} ${config_dir} ${seed}
  elif [[ -d /usatlas ]]
  then
    # There is a madgraph error; I can just raise a flag and have the process skip that step.
    local  output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/EVNT"
    local  config_dir="EVNTFiles/100xxx/100001/"
    local  OScontainer="centos7"
    cd /usatlas/workarea/jroblesgo
    Batch ${config_dir} ${seed}
  elif [[ -d /data ]]
  then
    local  output_dir="/data/selbor/benchmarks/$curr_date/EVNT/"
    local  config_dir="/data/selbor/evnt/100xxx/100001/"
    local  OScontainer="centos7"
    Batch ${config_dir} ${seed}
  fi
  mkdir -p ${output_dir}
  mv myjob.* ${output_dir}
  mv log.* ${output_dir}
  hostname >> ${output_dir}/log.*
  # I still need to get the payload size into the log file.
}

# Call the main function
main

