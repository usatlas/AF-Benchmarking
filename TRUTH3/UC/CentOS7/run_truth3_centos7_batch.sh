#!/bin/bash
# shellcheck disable=SC1091

curr_time=$(date +"%Y.%m.%dT%H")
# current time used for log file storage


# Defines the directory where the input files are stored
config_dir="${GITHUB_WORKSPACE}/TRUTH3/EVNT.root"

# Sets up the ATLAS Environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Appends time before Reco_tf.py to log file
date +'%H:%H:%S' >> split.log

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh -c centos7 -r "asetup AthDerivation,21.2.178.0,here && \
  Reco_tf.py --inputEVNTFile ${config_dir} --outputDAODFile=TRUTH3.root --reductionConf TRUTH3 2>&1 | tee pipe_file.log"

# Appends time after Reco_tf.py to a log file
date +'%H:%H:%S' >> split.log

# Defining the output directory
output_dir="/home/$(whoami)/benchmarks/${curr_time}/TRUTH3_centos/"

# Creates the output directory
mkdir -p "${output_dir}"

# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du DAOD_TRUTH3.TRUTH3.root >> split.log

# Moves the log file to the output directory
#mv log.EVNTtoDAOD "${output_dir}"
mv split.log "${output_dir}"
mv pipe_file.log "${output_dir}"

# Directory that needs to be cleaned
cleanup_dir="/home/selbor/TRUTH3Job/centos7"


if [[ -d "${cleanup_dir}" && "${cleanup_dir}" == "/home/selbor/TRUTH3Job/centos7" ]]; then
    rm -rf "${cleanup_dir:?}/"*
fi
