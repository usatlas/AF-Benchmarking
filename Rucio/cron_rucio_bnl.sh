#!/bin/bash

# Job directory
job_dir="/usatlas/u/jroblesgo/RucioJob"

if [ -d ${job_dir} ]; then
  cd "${job_dir}" || exit
  /usatlas/u/jroblesgo/AF-Benchmarking/Rucio/rucio_script.sh
fi
