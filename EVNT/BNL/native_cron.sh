#!/bin/bash

# Job directory
job_dir="/usatlas/u/jroblesgo/EVNTJob/native"

if [ -d ${job_dir} ]; then
  cd ${job_dir}
  condor_submit ~/AF-Benchmarking/EVNT/BNL/evnt_native.sub
fi
