#!/bin/bash

cd /sdf/scratch/users/s/selbor/benchmarks/TRUTH3Job/container_centos
rm *
sbatch /sdf/home/s/selbor/AF-Benchmarking/TRUTH3/benchmark_TRUTH_slac_c_c.sh
