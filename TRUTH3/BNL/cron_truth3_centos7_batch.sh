#! /bin/bash

# Changes to the directory made for the job
cd /atlasgpfs01/usatlas/scratch/jroblesgo/TRUTH3_centos_batch

# Submits the job to condor
condor_submit ~/AF-Benchmarking/TRUTH3/BNL/truth3_centos.sub
