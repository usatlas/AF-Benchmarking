#!/bin/bash

cd /home/selbor/ntuple/coffea || exit

condor_submit /home/selbor/AF-Benchmarking/NTuple_Hist/coffea/UC/coffea_el9.sub
