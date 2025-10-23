#!/bin/bash

cd /home/selbor/EVNTJob/native || exit

mkdir -p /scratch/selbor/EVNTJob/native/

condor_submit /home/selbor/AF-Benchmarking/EVNT/UC/Native/evnt_native.sub
