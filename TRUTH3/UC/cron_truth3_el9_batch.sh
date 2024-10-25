#!/bin/bash

cd /data/selbor/TRUTH3Job/container_el/

rm *

condor_submit /home/selbor/AF-Benchmarking/TRUTH3/UC/truth3_el.sub
