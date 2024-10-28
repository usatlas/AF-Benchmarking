#!/bin/bash


curr_time=$(date +"%Y.%m.%dT%H")

config_dir="TRUTH3Files/el9_interactive/"
OScontainer="el9"
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup Athena,24.0.53,here && \
Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

output_dir="/sdf/scratch/users/s/selbor/benchmarks/$curr_time/TRUTH3_el9_container_interactive"
mkdir -p ${output_dir}
hostname >> log.Derivation
du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
mv log.Derivation ${output_dir}
