#!/bin/bash

cd /home/selbor/ntuple/eventloop_noarrays/ || exit

condor_submit /home/selbor/AF-Benchmarking/NTuple_Hist/event_loop/UC/eventloop_noarrays.sub
