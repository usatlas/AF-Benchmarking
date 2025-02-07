#!/bin/bash
ssh iana "
cd /sdf/data/atlas/u/selbor/EVNTJob/container_el
rm *
sbatch /sdf/data/atlas/u/selbor/AF-Benchmarking/EVNT/SLAC/evnt_el9_sub.sh"
