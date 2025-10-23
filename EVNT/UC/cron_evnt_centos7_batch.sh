#!/bin/bash
cd /data/selbor/EVNTJob/container_centos || exit

rm ./*

condor_submit /home/selbor/AF-Benchmarking/EVNT/UC/evnt_centos7.sub
