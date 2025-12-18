#! /bin/bash

# Job directory
job_dir="$HOME/TRUTH3Job/native"

if [ -d "${job_dir}" ]; then
  cd "${job_dir}" || exit
  condor_submit ~/AF-Benchmarking/TRUTH3/BNL/Native/truth3_native.sub
fi
