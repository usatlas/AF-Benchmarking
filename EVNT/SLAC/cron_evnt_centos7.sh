#!/bin/bash
ssh iana "
cd /sdf/scratch/atlas/selbor/EVNTJob/container_centos
rm *
sbatch /sdf/scratch/atlas/selbor/AF-Benchmarking/EVNT/SLAC/evnt_centos7_sub.sh"
