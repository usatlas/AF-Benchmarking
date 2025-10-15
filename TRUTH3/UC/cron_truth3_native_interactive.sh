#!/bin/bash

cd /data/selbor/TRUTH3Job/native_interactive || exit

rm -r ./*

/home/selbor/AF-Benchmarking/TRUTH3/UC/run_truth3_native_interactive.sh
