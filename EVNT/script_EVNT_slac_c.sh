#!/bin/bash

cd /sdf/scratch/users/s/selbor/EVNTJob/container_centos
rm *
sbatch ~/AF-Benchmarking/EVNT/benchmark_EVNT_slac_c_c.sh
