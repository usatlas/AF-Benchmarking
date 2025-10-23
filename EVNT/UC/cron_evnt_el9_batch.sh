#!/bin/bash

cd /data/selbor/EVNTJob/container_el || exit

rm ./*

condor_submit /home/selbor/AF-Benchmarking/EVNT/UC/evnt_el9.sub
