#!/bin/bash
#
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J ff
#SBATCH --cpus-per-task=1
#SBATCH --constraint=cpu
#SBATCH --mail-type=ALL
#SBATCH -t 1:0:0
#SBATCH --mem=3GB

# OpenMP settings:
export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

srun -n 1 -c 1 --cpu_bind=cores  "$HOME"/AF-Benchmarking/NTuple_Hist/fastframes/NERSC/run_ff.sh
