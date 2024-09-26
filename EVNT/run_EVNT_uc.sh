#!/bin/bash


if [[ ${1} == '-b' ]]
then
  # UChicago uses the AthGeneration,23.6.34
  # Current time used for log file storage
  # curr_time=$(date +"%Y.%m.%dT%H")

  # The seed used in the job
  seed=1001

  # Directory storing the input files
  config_dir="/data/selbor/evnt/100xxx/100001"

  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  asetup AthGeneration,23.6.34,here
  Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir}  --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=${seed}

  # Directory where all the output files will be sent to
  output_dir="/data/selbor/benchmarks/$curr_date/EVNT/"

  mkdir -p ${output_dir}
  mv *.generate ${output_dir}
  mv myjob.* ${output_dir}
  hostname >> *.generate
  du EVNT.root >> *.generate
fi
