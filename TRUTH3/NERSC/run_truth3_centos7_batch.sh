#!/bin/bash


# Defines the OS the container will have
OScontainer="centos7"
cp ~/AF-Benchmarking/TRUTH3/EVNT.root .
# Sets up the working environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "asetup AthDerivation,21.2.178.0,here && \
  Reco_tf.py --inputEVNTFile EVNT.root --outputDAODFile=TRUTH3.root --reductionConf TRUTH3"

rm EVNT.root
