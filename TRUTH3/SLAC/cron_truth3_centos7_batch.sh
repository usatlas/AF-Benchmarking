#!/bin/bash
ssh iana "

cd /sdf/home/s/selbor/TRUTH3Job/container_centos

rm -r *

sbatch /sdf/data/atlas/u/selbor/AF-Benchmarking/TRUTH3/SLAC/truth3_centos7_sub.sh"
