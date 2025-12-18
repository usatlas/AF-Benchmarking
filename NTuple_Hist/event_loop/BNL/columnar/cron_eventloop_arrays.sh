#!/bin/bash

cd /atlasgpfs01/usatlas/data/jroblesgo/eventloopJob_arrays || exit

condor_submit /usatlas/u/jroblesgo/AF-Benchmarking/NTuple_Hist/event_loop/BNL/event_loop_arrays.sub
