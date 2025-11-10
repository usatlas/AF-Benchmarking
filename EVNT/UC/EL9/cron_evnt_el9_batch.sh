#!/bin/bash

cd /home/selbor/EVNTJob/el9 || exit

condor_submit /home/selbor/AF-Benchmarking/EVNT/UC/EL9/evnt_el9.sub
