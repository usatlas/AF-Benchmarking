#!/bin/bash

configdir=$PWD/100xxx/100001
cp /AF-Benchmarking/EVNT/mc* $configdir
cp /AF-Benchmarking/EVNT/SUSY_*.py $configdir

curr_time=$(date +"%Y.%m.%dT%H")

if [ $HOME = "/home/$USER" ]
then
  output_dir="/data/$USER/benchmarks/$curr_time/EVNT/"
elif [ $HOME = "/sdf/home/s/$USER" ]
then
  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT/"
elif [ $HOME = "/usatlas/u/$USER" ]
then 
  output_dir="/usatlas/workarea/$USER/benchmarks/$curr_time/EVNT"
fi


export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
asetup AthGeneration,23.6.34,here

seed=1001

Gen_tf.py --ecmEnergy=13000.0 --jobConfig=$configdir  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}

mkdir -p $output_dir


mv log.* ${outputdir}
mv *.generate ${outputdir}
mv evnt.* ${outputdir}
