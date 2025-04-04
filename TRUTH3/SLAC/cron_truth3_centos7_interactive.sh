#!/bin/bash

ssh iana "
cd /sdf/home/s/selbor/TRUTH3_int/centos

rm -r *

./AF-Benchmarking/TRUTH3/SLAC/run_truth3_centos7_interactive.sh"
