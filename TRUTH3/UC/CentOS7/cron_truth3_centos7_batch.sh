#!/bin/bash

cd /home/selbor/TRUTH3Job/centos7/ || exit

condor_submit /home/selbor/AF-Benchmarking/TRUTH3/UC/CentOS7/truth3_centos7.sub
