#!/bin/bash

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
inputdir=/data/selbor/TRUTH3_centos7_batch_StaticDir/
outputdir=/home/selbor/benchmarks/benchmark_TRUTH_centos7/100xxx/100001/
seed=1001

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -b -c centos7 -m /data:/data -r "asetup AthDerivation,21.2.178.0,here && \
Reco_tf.py --inputEVNTFile ${inputdir}EVNT_centos.root --outputDAODFile TRUTH3.root --reductionConf TRUTH3" 

mkdir -p ${outputdir}

