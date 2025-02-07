#!/bin/bash
ssh iana "
cd /sdf/data/atlas/u/selbor/EVNTJob/container_centos
rm *
sbatch /sdf/data/atlas/u/selbor/AF-Benchmarking/EVNT/SLAC/evnt_centos7_sub.sh"
