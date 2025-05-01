#!/bin/bash
# current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")



# Defines the OS the container will have
OScontainer="centos7"
job_dir="$SCRATCH/TRUTH3/centos_int/"
mkdir -p ${job_dir}
cd ${job_dir}
cp ~/AF-Benchmarking/TRUTH3/EVNT.root .
# Sets up the working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Appends time before Reco_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthDerivation,21.2.178.0,here && \
  Reco_tf.py --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3 2>&1 | tee pipe_file.log"

# Appends time after Reco_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

rm EVNT.root

# Defining the output directory
output_dir="$HOME/benchmarks/$curr_time/TRUTH3_centos_int/"

# Creates the output directory
mkdir -p ${output_dir}

# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du DAOD_TRUTH3.TRUTH3.root >> split.log

# Moves the log file to the output directory
mv log.EVNTtoDAOD ${output_dir}
mv split.log ${output_dir}
mv pipe_file.log ${output_dir}

rm *
