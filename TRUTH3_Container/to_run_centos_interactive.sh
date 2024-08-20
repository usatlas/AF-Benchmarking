#!/bin/bash

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
curr_time=$(date +"%Y.%m.%dT%H")
if [ $HOME = "/home/$USER" ]
then
  inputdir=/data/selbor/TRUTH3_centos7_interactive_StaticDir/
  outputdir=/data/selbor/benchmarks/$curr_time/truth3_centos_interactive
elif [ $HOME = "/sdf/home/s/$USER" ]
then
  inputdir=$HOME/AF-Benchmarking/TRUTH3_Container/
  outputdir=/sdf/data/atlas/u/selbor/benchmarks/$curr_time/truth3_centos7_interactive/
fi

mkdir -p ${outputdir}

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -b -c centos7 -m /data:/data -r "asetup AthDerivation,21.2.178.0,here && \
Reco_tf.py --inputEVNTFile ${inputdir}EVNT_centos.root --outputDAODFile TRUTH3.root --reductionConf TRUTH3" 2>&1 | tee ${outputdir}$curr_time.log


du *.root >> ${outputdir}$curr_time.log
hostname >> ${outputdir}$curr_time.log

mv *.root ${outputdir}
mv log.EVNTtoDAOD ${outputdir} 
rm *
