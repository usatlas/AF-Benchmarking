#!/bin/bash
ssh iana "
cd /sdf/home/s/selbor/EVNTJob/container_centos || exit
rm ./*
sbatch /sdf/home/s/selbor/AF-Benchmarking/EVNT/SLAC/evnt_centos7_sub.sh"
