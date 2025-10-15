#!/bin/bash

# Job directory
job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/EVNT/el"

if [ -d ${job_dir} ]; then
  cd "${job_dir}" || exit
  condor_submit ~/AF-Benchmarking/EVNT/BNL/evnt_el.sub
fi
