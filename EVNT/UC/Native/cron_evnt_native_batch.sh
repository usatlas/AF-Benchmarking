#!/bin/bash

cd /home/selbor/EVNTJob/native || exit

condor_submit /home/selbor/AF-Benchmarking/EVNT/UC/native/evnt_native.sub
