#!/bin/bash

# Sets up ATLAS environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets up root and boost
asetup StatAnalysis,0.5.0

# Sets up emi
lsetup emi

# Gives certificate credentials
cat $HOME/pass.txt | voms-proxy-init -voms atlas

lsetup "rucio -w"

# Job's directory
cd $DATA/ntuple_hist/FastFrames/

# Go into the class's build directory
cd /data/$USER/ntuple_hist/TutorialClass/build

# Setting paths
source setup.sh

# Return to the job's directory
cd -

# Set output path as $HOME due to permission issues
cat $HOME/ff_local_GD.txt | python3 python/produce_metadata_files.py --grid_datasets $HOME/input/rucio_input.txt --output_path $HOME/input/
