#!/bin/bash

cd /sdf/scratch/users/s/selbor/EVNTJob/container_el
rm *
sbatch ~/AF-Benchmarking/EVNT/benchmark_EVNT_slac_c_e.sh
