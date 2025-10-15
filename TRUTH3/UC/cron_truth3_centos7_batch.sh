#!/bin/bash

cd /data/selbor/TRUTH3Job/container_centos/ || exit || exit

rm ./*

condor_submit /home/selbor/AF-Benchmarking/TRUTH3/UC/truth3_centos7.sub
