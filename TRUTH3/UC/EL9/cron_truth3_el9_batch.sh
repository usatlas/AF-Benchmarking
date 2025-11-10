#!/bin/bash

cd /home/selbor/TRUTH3Job/el9/ || exit

condor_submit /home/selbor/AF-Benchmarking/TRUTH3/UC/EL9/truth3_el9.sub
