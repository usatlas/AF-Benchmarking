#!/bin/bash

# Base script generated by NERSC Batch Script Generator on https://iris.nersc.gov/jobscript.html

#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J truth3_centos7
#SBATCH --mail-user=jprobles@ucsc.edu
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=128
#SBATCH --constraint=cpu
#SBATCH -t 1:0:0
#SBATCH --mem=4GB

# OpenMP settings:
export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

#run the application: 
srun -n 1 -c 256 --cpu_bind=cores  $HOME/AF-Benchmarking/TRUTH3/NERSC/run_truth3_centos7_batch.sh