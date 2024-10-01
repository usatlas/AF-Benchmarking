#!/bin/bash
cd /data/selbor/EVNTJob/container_el
rm *
condor_submit ~/AF-Benchmarking/EVNT/benchmark_EVNT_uc_e.sub
