
#!/bin/bash

curr_time=$(date +"%Y.%m.%dT%H")
# checks the home directory to determine the AF
# /home/$USER is for UC
if [[ $1 == "/home/$USER" ]]
then
  output_dir="/data/$USER/benchmarks/$curr_time/EVNT/"
# /sdf/home/s/$USER is for SLAC
elif [[ $1 == "/sdf/home/s/$USER" ]]
then
  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT"
# /usatlas/u/$USER is for BNL
elif [[ $1 == "/usatlas/u/$USER" ]]
then
  #working_dir="/usatlas/workarea/jroblesgo/"
  configdir=/usatlas/u/$USER/AF-Benchmarking/EVNT/
  output_dir="/usatlas/workarea/$USER/benchmarks/$curr_time/EVNT"
fi

seed=1001
echo ${configdir}
# Checks the input parameter; BNL & SLAC
if [[ $2 == "c" ]]
then
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -b -c el9 -r "asetup AthGeneration,23.6.34,here && \
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${configdir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}"
  elif [[ $2 == "n" ]]
  then
    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
    source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
    asetup AthGeneration,23.6.34,here
    Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${configdir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}
fi

mkdir -p ${output_dir}

mv log.* ${output_dir}
mv *.generate ${output_dir}
mv evnt.* ${output_dir}

