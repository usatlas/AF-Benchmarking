#!/bin/bash

cd /sdf/scratch/users/s/selbor/EVNTJob/container_centos
rm *
sbatch /sdf/home/s/selbor/AF-Benchmarking/EVNT/SLAC/run_evnt_centos_container.sh
