#!/bin/bash

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/eventloop_noarrays || exit

condor_submit /usatlas/u/jroblesgo/AF-Benchmarking/NTuple_Hist/event_loop/BNL/standard/eventloop_noarrays.sub
