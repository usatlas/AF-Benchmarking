#!/bin/bash

# Moves to the data directory
cd /data/$USER/MWE/

# Prints the directory the job is started at
pwd 2>&1 | tee mwe.log

# Prints the items at the directory
ls >> mwe.log

cp /data/$USER/TRUTH3_StaticDir/EVNT.root .

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

