#!/bin/bash

ssh iana "
cd /sdf/data/atlas/u/selbor/TRUTH3Job/container_el

rm -r *

sbatch /sdf/data/atlas/u/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_el9_sub.sh"
