#!/bin/bash

cd /data/selbor/TRUTH3Job/container_el_interactive/ || exit

rm ./*

/home/selbor/AF-Benchmarking/TRUTH3/UC/run_truth3_el9_interactive.sh
