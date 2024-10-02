#!/bin/bash

cd /sdf/scratch/atlas/selbor/TRUTH3Job/container_el
rm *
sbatch ~/AF-Benchmarking/TRUTH3/benchmark_TRUTH_slac_c_e.sh
