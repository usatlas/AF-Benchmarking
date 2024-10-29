#!/bin/bash

config_dir="/home/selbor/TRUTH3Files/el9_interactive/"
OScontainer="el9"
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "cp -r /home/selbor/TRUTH3Files/ && \
asetup Athena,24.0.53,here && \
Derivation_tf.py --CA True --inputEVNTFile /srv/TRUTH3Files/el9_interactive/EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

curr_time=$(date +"%Y.%m.%dT%H")
output_die="/home/selbor/benchmarks/${curr_time}/TRUTH3_el9_container_interactive"
mkdir -p ${output_dir}
hostname >> log.Derivation
du DAOD_TRUTH3.TRUTH3.root >> log.Derivation
mv log.Derivation ${output_dir}
