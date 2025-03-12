#! /bin/bash

# Job directory
job_dir="/usatlas/u/jroblesgo/TRUTH3Job/centos_i"

if [ -d ${job_dir} ]; then
  cd ${job_dir}
  /usatlas/u/jroblesgo/AF-Benchmarking/TRUTH3/BNL/run_truth3_centos7_interactive.sh
fi

