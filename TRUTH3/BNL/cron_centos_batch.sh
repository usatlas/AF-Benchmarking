#! /bin/bash

# Job directory
job_dir="/usatlas/u/jroblesgo/TRUTH3Job/centos"

if [ -d ${job_dir} ]; then
  cd ${job_dir}
  condor_submit ~/AF-Benchmarking/TRUTH3/BNL/truth3_centos.sub
fi

