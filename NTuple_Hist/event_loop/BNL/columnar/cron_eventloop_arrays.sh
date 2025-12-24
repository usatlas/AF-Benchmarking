#!/bin/bash

cd /atlasgpfs01/usatlas/scratch/jroblesgo/ntuple/eventloop_arrays || exit

condor_submit ~/AF-Benchmarking/NTuple_Hist/event_loop/BNL/columnar/eventloop_arrays.sub
