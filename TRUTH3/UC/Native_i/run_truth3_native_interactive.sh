#!/bin/bash
# shellcheck disable=SC1091

# current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Input files are stored here
config_dir="/data/$USER/TRUTH3_StaticDir/"

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh

# Appends time before Derivation_tf.py to log file
date +'%H:%H:%S' >> split.log

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile "${config_dir}EVNT_interactive.root" --outputDAODFile=TRUTH3.root --formats TRUTH3 2>&1 | tee pipe_file.log

# Appends time after Derivation_tf.py to a log file
date +'%H:%H:%S' >> split.log

# Defines the output directory
output_dir="/home/$USER/benchmarks/${curr_time}/TRUTH3_interactive"

# Creates the output directory
mkdir -p "${output_dir}"

# Obtains and appends the host machine and payload size to the log file
hostname >> split.log
du DAOD_TRUTH3.TRUTH3.root >> split.log

# Moves the log file to the output directory
mv log.Derivation "${output_dir}"
mv split.log "${output_dir}"
mv pipe_file.log "${output_dir}"

# Directory that needs to be cleaned
cleanup_dir="/home/selbor/TRUTH3Job/native_i"

if [[ -d "${cleanup_dir}" && "${cleanup_dir}" == "/home/selbor/TRUTH3Job/native_i" ]]; then
    rm -rf "${cleanup_dir:?}/"*
fi
