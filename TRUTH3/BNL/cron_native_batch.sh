#! /bin/bash

# Job directory
job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/TRUTH3/native"

if [ -d ${job_dir} ]; then
  cd "${job_dir}" || exit
  condor_submit ~/AF-Benchmarking/TRUTH3/BNL/truth3_native.sub
fi
