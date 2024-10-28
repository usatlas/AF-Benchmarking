#!/bin/bash

cd /sdf/scratch/users/s/selbor/TRUTH3Job/container_centos

rm *

sbatch /sdf/home/s/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_centos7.sh
