#!/bin/bash
  
OS_container="centos7"

# The seed used in the job
seed=1001

# Directory storing the input files
config_dir="/data/$(whoami)/evnt_centos/100xxx/100001"

# Creates the ATLAS Environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Appends time before Gen_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -m /data:/data -r "asetup AthGeneration,23.6.31,here && export LHAPATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current:/cvmfs/atlas.cern.ch/repo/sw/software/23.6/sw/lcg/releases/LCG_104d_ATLAS_13/MCGenerators/lhapdf/6.5.3/x86_64-centos7-gcc11-opt/share/LHAPDF:/cvmfs/atlas.cern.ch/repo/sw/Generators/lhapdfsets/current && export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current:/cvmfs/atlas.cern.ch/repo/sw/software/23.6/sw/lcg/releases/LCG_104d_ATLAS_13/MCGenerators/lhapdf/6.5.3/x86_64-centos7-gcc11-opt/share/LHAPDF:/cvmfs/atlas.cern.ch/repo/sw/Generators/lhapdfsets/current && Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir} --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=1001"

# Appends time after Gen_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines and makes the output directory
output_dir="/data/$(whoami)/benchmarks/$curr_time/EVNT_contained_centos7/"
mkdir -p ${output_dir}

# Appends the hostname and payload size to the log files
hostname >> split.log
du EVNT.root >> split.log

# Moves the log file to the output directory
mv log.generate ${output_dir}
mv split.log ${output_dir}
