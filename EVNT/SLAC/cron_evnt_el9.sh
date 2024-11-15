#!/bin/bash
ssh iana "
cd /sdf/scratch/users/s/selbor/EVNTJob/container_el
rm *
sbatch /sdf/home/s/selbor/AF-Benchmarking/EVNT/SLAC/evnt_el9_sub.sh"
