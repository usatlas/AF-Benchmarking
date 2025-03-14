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

# Go into the class's build directory
cd /data/$USER/ntuple_hist/TutorialClass/build

# Setting paths
source setup.sh

# Return to the job's directory
cd -

# Getting the date and time before running script
echo date >> ff.log

# Running the FastFrames script
python3 /data/$USER/ntuple_hist/FastFrames/python/FastFrames.py -c $HOME/AF-Benchmarking/NTuple_Hist/fastframes/example_config.yml 2>&1 | tee ff.log

# Getting the date and time after running script
echo date >> ff.log
