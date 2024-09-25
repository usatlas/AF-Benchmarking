#!/bin/bash

# Location of input files
config_dir="$HOME/EVNTFiles/100xxx/100001"

# OS used in the container
OScontainer="centos7"

# The seed used in the job
seed=1001
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthGeneration,23.6.31,here && \
Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}"

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")

output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT"

mkdir -p ${output_dir}
mv log.* ${output_dir}
#hostname >> ${output_dir}/log.generate
mv myjob.* ${output_dir}

