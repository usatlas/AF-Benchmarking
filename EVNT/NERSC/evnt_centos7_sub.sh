#!/bin/bash

# Base script generated by NERSC Batch Script Generator on https://iris.nersc.gov/jobscript.html

#SBATCH -N 2
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J evnt_centos7
#SBATCH --mail-user=jprobles@ucsc.edu
#SBATCH --mail-type=ALL
#SBATCH -t 2:0:0

# OpenMP settings:
export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

#run the application: 
srun -n 2 -c 256 --cpu_bind=cores  $HOME/AF-Benchmarking/EVNT/NERSC/run_evnt_centos7_batch.sh