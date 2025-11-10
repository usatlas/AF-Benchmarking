#!/bin/bash
cd /home/selbor/EVNTJob/centos7 || exit

condor_submit /home/selbor/AF-Benchmarking/EVNT/UC/CentOS7/evnt_centos7.sub
