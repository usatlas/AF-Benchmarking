#! /bin/bash

# Job directory
job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/TRUTH3/el_int/"

if [ -d ${job_dir} ]; then
  cd ${job_dir}
  /usatlas/u/jroblesgo/AF-Benchmarking/TRUTH3/BNL/run_truth3_el9_interactive.sh
fi

