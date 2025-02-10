#!/bin/bash
ssh iana "
cd /sdf/scratch/atlas/selbor/EVNTJob/container_el
rm *
sbatch /sdf/scratch/atlas/selbor/AF-Benchmarking/EVNT/SLAC/evnt_el9_sub.sh"
