#! /bin/bash

# Job directory
job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/TRUTH3/centos"

if [ -d ${job_dir} ]; then
  cd "${job_dir}" || exit
  condor_submit ~/AF-Benchmarking/TRUTH3/BNL/CentOS7/truth3_centos.sub
fi
