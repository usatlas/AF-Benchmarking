#!/bin/bash

ssh iana "
cd /sdf/home/s/selbor/TRUTH3Job/container_el || exit

rm -r ./*

sbatch /sdf/home/s/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_el9_sub.sh"
