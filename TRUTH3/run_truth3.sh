#!/bin/bash
curr_date=$(date +"%Y.%m.%dT%H")

if [ $HOME = "/home/$USER"]
then
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  inputdir="/data/selbor/TRUTH3_StaticDir/"
  outputdir="/data/selbor/benchmarks/$curr_date/TRUTH3/"
elif [ $HOME = "/sdf/home/s/$USER"]
then
  inputdir="/sdf/home/s/selbor/AF-Benchmarking/TRUTH3/"
  outputdir="/sdf/data/atlas/u/$USER/benchmarks/$curr_date/TRUTH3/"
fi

# This same block works at SLAC
# But it doesn't seem to run at BNL
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
asetup Athena,24.0.53,here

Derivation_tf.py --CA True --inputEVNTFile ${inputdir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3


mkdir -p ${outputdir}

mv log.EVNTtoDAOD ${outputdir}
mv log.Derivation ${outputdir}

#mv /data/selbor/TRUTH3/* ${outputdir}
