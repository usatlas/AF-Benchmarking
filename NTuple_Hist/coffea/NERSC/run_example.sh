#!/bin/bash

# Run this in a container

cd #Job Directory used

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "lsetup 'python 3.9.21-x86_64-centos7' &&\

  python3 ./AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py
"
