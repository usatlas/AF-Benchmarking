#!/bin/bash

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/coffea

source ../bin/activate/

setupATLAS

lsetup "python 3.9.21-x86_64-centos7"

python3 /usatlas/u/jroblesgo/AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py
