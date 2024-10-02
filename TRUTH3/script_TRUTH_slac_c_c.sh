#!/bin/bash

ssh iana
cd /sdf/scratch/users/s/selbor/TRUTH3Job/container_centos
rm *
sbatch ~/AF-Benchmarking/TRUTH3/benchmark_TRUTH_slac_c_c.sh
