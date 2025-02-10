#!/bin/bash

ssh iana "
cd /sdf/scratch/atlas/selbor/TRUTH3Job/container_el

rm -r *

sbatch /sdf/scratch/atlas/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_el9_sub.sh"
