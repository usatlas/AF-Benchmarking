#!/bin/bash

cd /data/selbor/TRUTH3Job/native/

rm *

condor_submit /home/selbor/AF-Benchmarking/TRUTH3/UC/truth3_native.sub
