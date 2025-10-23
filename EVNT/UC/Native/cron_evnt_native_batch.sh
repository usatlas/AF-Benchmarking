#!/bin/bash

cd /home/selbor/EVNTJob/native || exit

condor_submit /home/selbor/AF-Benchmarking/EVNT/UC/evnt_native.sub
