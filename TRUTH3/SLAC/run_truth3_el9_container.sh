#!/bin/bash


curr_time=$(date +"%Y.%m.%dT%H")

config_dir="TRUTH3Files/"
OScontainer="el9"
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
echo "The container is started" >> $HOME/truth3.${curr_time}.txt
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup Athena,24.0.53,here && \
Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3 2>&1 | tee $HOME/truth3.${curr_time}.txt"

output_dir="/sdf/scratch/users/s/selbor/benchmarks/$curr_time/TRUTH3_el9_container"
mkdir -p ${output_dir}
hostname >> log.EVNTtoDAOD
du DAOD_TRUTH3.TRUTH3.root >> log.EVNTtoDAOD
mv log.EVNTtoDAOD ${output_dir}
