#!/bin/bash

cd /data/selbor/TRUTH3Job/centos_interactive || exit

rm ./*

/home/selbor/AF-Benchmarking/TRUTH3/UC/run_truth3_centos7_interactive.sh
