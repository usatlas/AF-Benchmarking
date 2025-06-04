#!/bin/bash

curr_date=$(date +"%Y.%m.%dT%H")

cd /atlasgpfs01/usatlas/data/jroblesgo/

# Sets up ATLAS environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -r "asetup StatAnalysis,0.5.0 &&\
  cmake3 -S /srv/FastFrames -B /srv/FastFrames/build -DCMAKE_INSTALL_PREFIX=/srv/FastFrames/install &&\
  cmake3 --build /srv/FastFrames/build -j 16 --target install &&\
  source /srv/FastFrames/build/setup.sh &&\
  cmake3 -S /srv/TutorialClass -B /srv/TutorialClass/build -DCMAKE_PREFIX_PATH=/srv/FastFrames/install -DCMAKE_INSTALL_PREFIX=/srv/TutorialClass/install &&\
  cmake3 --build /srv/TutorialClass/build -j 16 --target install &&\
  source /srv/TutorialClass/build/setup.sh &&\

  cmake3 -S /srv/TutorialClass/ -B /srv/TutorialClass/build &&\
  cmake3 --build /srv/TutorialClass/build -j 16 &&\
  source /srv/TutorialClass/build/setup.sh &&\
  echo date >> ff.log &&\
  python3 /srv/FastFrames/python/FastFrames.py -c /srv/input/example_config.yml 2>&1 | tee ff.log"
date >> ff.log
hostname >> ff.log

# output directory
#output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_date/FF_NTuple"

# Creates output dir
#mkdir -p ${output_dir}

# Moves log to outputdir
#mv ff.log ${output_dir}
mv ff.log $HOME
