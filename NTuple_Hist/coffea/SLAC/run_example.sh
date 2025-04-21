#!/bin/bash

# Setting up environment and container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

export ALRB_localConfigDir=$HOME/localConfig

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -m /sdf/data/atlas/ -r "python3 example.py"
