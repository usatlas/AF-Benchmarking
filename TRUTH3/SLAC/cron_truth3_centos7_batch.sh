#!/bin/bash
ssh iana "

cd /sdf/scratch/users/s/selbor/TRUTH3Job/container_centos

rm -r *

sbatch /sdf/home/s/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_centos7_sub.sh"
