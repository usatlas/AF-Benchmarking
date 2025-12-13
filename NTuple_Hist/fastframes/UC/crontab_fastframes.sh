#!/bin/bash

cd /home/selbor/ntuple/ff/ || exit

condor_submit /home/selbor/AF-Benchmarking/NTuple_Hist/fastframes/UC/fastframes_el9.sub
