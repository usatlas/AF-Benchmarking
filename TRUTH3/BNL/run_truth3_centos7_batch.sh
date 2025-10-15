#!/bin/bash
# current time used for log file storage

curr_time=$(date +"%Y.%m.%dT%H")

# Copying input files to working directory
cp -r ~/AF-Benchmarking/TRUTH3/EVNT.root .

# Sets up the ATLAS Environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh -c centos7 -r "asetup AthDerivation,21.2.178.0,here && \
  date +'%Y.%m.%d.%H.%S' >> split.log &&\
  Reco_tf.py --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3 2>&1 | tee pipe_file.log &&\
  date +'%Y.%m.%d.%H.%S'"

output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/${curr_time}/TRUTH3_centos7_batch"

mkdir -p "${output_dir}"

hostname >> split.log
du DAOD_TRUTH3.TRUTH3.root >> split.log
# Moves the log file to the output directory
mv log.EVNTtoDAOD "${output_dir}"
mv split.log "${output_dir}"
mv pipe_file.log "${output_dir}"

# Checks the directory, if it matches it cleans it for the next job
if [ "$(pwd)" = "/atlasgpfs01/usatlas/scratch/jroblesgo/TRUTH3/centos" ]; then
  rm -r ./*
fi
