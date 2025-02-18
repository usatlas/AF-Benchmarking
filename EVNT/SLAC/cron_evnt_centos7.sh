#!/bin/bash
ssh iana "
cd /sdf/home/s/selbor/EVNTJob/container_centos
rm *
sbatch /sdf/data/atlas/u/selbor/AF-Benchmarking/EVNT/SLAC/evnt_centos7_sub.sh"
