#!/bin/bash
ssh iana "
cd \$HOME/EVNTJob/container_el || exit
rm ./*
sbatch \$HOME/AF-Benchmarking/EVNT/SLAC/EL9/evnt_el9_sub.sh"
