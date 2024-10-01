#!/bin/bash
cd /data/selbor/EVNTJob/container_centos
rm *
condor_submit ~/AF-Benchmarking/EVNT/benchmark_EVNT_uc_c.sub
