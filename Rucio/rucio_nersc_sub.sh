#!/bin/bash -l
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J rucio
#SBATCH --mail-user=jprobles@ucsc.edu
#SBATCH --mail-type=ALL
#SBATCH -t 00:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4

set -euo pipefail

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

cd "$HOME/AF-Benchmarking/Rucio"

srun --ntasks="${SLURM_NTASKS}" --cpus-per-task="${SLURM_CPUS_PER_TASK}" --cpu_bind=cores \
  "$HOME/AF-Benchmarking/Rucio/rucio_script.sh"
