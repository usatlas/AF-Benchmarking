#!/bin/bash
ssh iana "
cd \$HOME/EVNTJob/container_centos || exit
rm ./*
sbatch \$HOME/AF-Benchmarking/EVNT/SLAC/CentOS7/evnt_centos7_sub.sh"
