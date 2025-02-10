#!/bin/bash
ssh iana "

cd /sdf/scratch/atlas/selbor/TRUTH3Job/container_centos

rm -r *

sbatch /sdf/scratch/atlas/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_centos7_sub.sh"
