#!/bin/bash

config_dir=$HOME/TRUTH3Files/
OScontainer="el9"

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup Athena,24.0.53,here && \
  Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

curr_time=$(date +"%Y.%m.%dT%H")
output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/TRUTH3"
mkdir -p ${output_dir}
hostname >> *.generate
du TRUTH3.root >> *.generate
mv myjob.* ${output_dir}
mv log.* ${output_dir}



