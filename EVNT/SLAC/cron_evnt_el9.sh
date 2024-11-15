#!/bin/bash
ssh iana "
cd /sdf/scratch/users/s/selbor/EVNTJob/container_el
rm *
sbatch /sdf/home/s/selbor/AF-Benchmarking/EVNT/SLAC/run_evnt_el_container.sh"
