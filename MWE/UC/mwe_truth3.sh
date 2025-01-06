#!/bin/bash

# Having it run the job in this directory
cd /data/$USER/MWE

echo $USER

user_name=$(USER)

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here

echo $USER
echo $user_name

Derivation_tf.py --CA True --inputEVNTFile /data/${user_name}/TRUTH3_StaticDir/EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

