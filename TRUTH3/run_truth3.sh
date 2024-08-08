#!/bin/bash

configdir=$PWD/100xxx/100001

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
asetup Athena,24.0.53,here

inputdir="/data/selbor/TRUTH3_StaticDir/"
seed=1001


Derivation_tf.py --CA True --inputEVNTFile ${inputdir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3


outputdir="/home/selbor/benchmarks/benchmark_TRUTH/100xxx/100001/"
mkdir -p ${outputdir}
cp -a * ${outputdir}
