#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

cd /data/selbor/FFJob/

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

# Getting the host-machine's name
echo hostname >> ff.log

# output directory
output_dir="/data/$USER/benchmarks/${curr_date}/FF_NTuple"

# Creates output dir
mkdir -p ${output_dir}

# Moves log to outputdir
mv ff.log ${output_dir}
