#!/bin/bash

cd /home/selbor/TRUTH3Job/native/ || exit

condor_submit /home/selbor/AF-Benchmarking/TRUTH3/UC/Native/truth3_native.sub
