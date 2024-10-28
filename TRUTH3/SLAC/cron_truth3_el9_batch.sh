#!/bin/bash

cd /sdf/scratch/users/s/selbor/TRUTH3Job/container_el

rm *

sbatch ~/AF-Benchmarking/TRUTH3/SLAC/truth3_el9.sh
