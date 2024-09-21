#!/bin/bash
Container {
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -b -c ${1} -m ${2} -r "asetup AthDerivation,21.2.178.0,here && \
  Reco_tf.py --inputEVNTFile ${3}EVNT_centos.root --outputDAODFile TRUTH3.root --reductionConf TRUTH3" 
}
mkdir -p ${outputdir}

# Using a centos7 container for UChicago
# Mounting /data:/data for UChicago
# Input dir for Uchicago is inputdir=/data/selbor/TRUTH3_centos7_batch_StaticDir/
# Output dir for UChicago is outputdir=/home/selbor/benchmarks/benchmark_TRUTH_centos7/100xxx/100001/


main() {
  # Current time used for log file storage
  curr_time=$(date +"%Y.%m.%dT%H")
  # The seed used in the job

  # Checks for the home directory
  if [[ -d /sdf ]]; then
    local  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT"
    local  config_dir="$HOME/EVNTFiles/100xxx/100001"
    local  OScontainer="centos7"
    Batch ${config_dir} ${seed}
  elif [[ -d /usatlas ]]
  then
    # There is a madgraph error; I can just raise a flag and have the process skip that step.
    local  output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/EVNT"
    local  config_dir="EVNTFiles/100xxx/100001/"
    local  OScontainer="centos7"
    local  job_dir="/tmp/jroblesgo"
    Container ${OScontainer} ${job_dir} ${config_dir} ${seed}
  elif [[ -d /data ]]
  then
    local output_dir="/home/selbor/benchmarks/benchmark_TRUTH_centos7/100xxx/100001/"
    local config_dir="/data/selbor/TRUTH3_centos7_batch_StaticDir/"
    local OScontainer="centos7"
    local mounting="/data:/data"
    Container ${OScontainer} ${mounting} ${config_dir} 
  fi
  mkdir -p ${output_dir}
  mv log.* ${output_dir}
  #hostname >> ${output_dir}/log.generate
  mv myjob.* ${output_dir}
  # I still need to get the payload size into the log file.
}

# Call the main function
main
