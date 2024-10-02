#!/bin/bash

ssh iana
cd /sdf/scratch/users/s/selbor/TRUTH3Job/interactive_centos
rm *
~/AF-Benchmarking/TRUTH3/run_truth3_slac.sh c
