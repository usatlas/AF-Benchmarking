#!/bin/bash


# The seed used in the job
seed=1001

# Directory where the input files are stored
config_dir="EVNTFiles/100xxx/100001/"

# The OS used in the container
OScontainer="centos7"

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthGeneration,23.6.31,here &&\
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=100 --randomSeed=${seed}"

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Output directory
output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/EVNT_centos7_batch"

mkdir -p ${output_dir}
hostname >> log.generate
du EVNT.root >> log.generate
mv log.generate ${output_dir}
