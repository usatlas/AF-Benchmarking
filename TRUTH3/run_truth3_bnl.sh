#!/bin/bash


OScontainer="el9"

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "cp /usatlas/u/jroblesgo/TRUTH3Files/EVNT.root . && \ 
  asetup Athena,24.0.53,here && \
  Derivation_tf.py --CA True --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

curr_time=$(date +"%Y.%m.%dT%H")
# There is a madgraph error; I can just raise a flag and have the process skip that step.
output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/TRUTH3"
mkdir -p ${output_dir}
hostname >> log.generate
du TRUTH3.root >> log.generate
mv myjob.* ${output_dir}
mv log.* ${output_dir}
 

