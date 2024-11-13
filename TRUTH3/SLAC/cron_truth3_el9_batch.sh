#!/bin/bash

roh

cd /sdf/scratch/users/s/selbor/TRUTH3Job/container_el

rm -r *

sbatch /sdf/home/s/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_el9_sub.sh
