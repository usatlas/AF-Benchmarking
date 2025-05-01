#!/bin/bash

# Job directory
job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/EVNT/centos"

if [ -d ${job_dir} ]; then
  cd ${job_dir}
  condor_submit ~/AF-Benchmarking/EVNT/BNL/evnt_centos.sub
fi
