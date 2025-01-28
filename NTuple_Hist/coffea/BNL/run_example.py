#!/bin/bash

# Run this in a container

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/coffea

setupATLAS

lsetup "python 3.9.21-x86_64-centos7"

python3 /usatlas/u/jroblesgo/AF-Benchmarking/NTuple_Hist/coffea/BNL/example.py
