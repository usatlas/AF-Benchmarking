#!/bin/bash
cd /data/selbor/EVNTJob/native
rm *
condor_submit ~/AF-Benchmarking/EVNT/benchmark_EVNT_uc_n.sub
