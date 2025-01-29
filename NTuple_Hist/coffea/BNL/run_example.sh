#!/bin/bash

# Run this in a container

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/coffea

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

setupATLAS
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c centos7 -r "

lsetup "python 3.9.21-x86_64-centos7"

python3 /usatlas/u/jroblesgo/AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py
"
