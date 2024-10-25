#!/bin/bash

cd /data/selbor/EVNTJob/native

rm *

condor_submit /home/selbor/AF-Benchmarking/UC/evnt_native.sub
