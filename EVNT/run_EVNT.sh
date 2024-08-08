#!/bin/bash

configdir=$PWD/100xxx/100001

mkdir -p $configdir
cp /data/selbor/ReqFiles/mc* $configdir
cp /data/selbor/ReqFiles/SUSY_*.py $configdir

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
asetup AthGeneration,23.6.34,here

seed=1001

Gen_tf.py --ecmEnergy=13000.0 --jobConfig=$configdir  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}

outputdir="/home/selbor/benchmarks/benchmark_EVNT/100xxx/100001/"
mkdir -p ${outputdir}
cp -a * ${outputdir}

