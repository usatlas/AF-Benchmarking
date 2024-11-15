#!/bin/bash
ssh iana "
cd /sdf/scratch/users/s/selbor/EVNTJob/container_centos
rm *
sbatch /sdf/home/s/selbor/AF-Benchmarking/EVNT/SLAC/evnt_centos7_sub.sh"
