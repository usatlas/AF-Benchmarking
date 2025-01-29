#!/bin/bash

# Run this in a container

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/coffea

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "export ALRB_pythonVersion=3.9.21-x86_64-centos7 &&\

  lsetup root &&\

  python3 /usatlas/u/jroblesgo/AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py
"
