#!/bin/bash
ssh iana "
cd /sdf/home/s/selbor/EVNTJob/container_el
rm *
sbatch /sdf/home/s/selbor/AF-Benchmarking/EVNT/SLAC/evnt_el9_sub.sh"
