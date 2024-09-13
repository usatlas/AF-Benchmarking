#!/bin/bash
#
#SBATCH --account=atlas:usatlas
#SBATCH --partition=ampere
#SBATCH --gpus a100:1
#SBATCH --job-name=truth3_batch
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=4g
#SBATCH --time=0-00:30:00


export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase 

# Use ALRB_CONT_CMDOPTS to provide bind mount, etc. options 

export ALRB_CONT_CMDOPTS="-B /sdf"

export ALRB_CONT_RUNPAYLOAD="source $HOME/AF-Benchmarking/TRUTH3/run_truth3.sh"

source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -c centos7 –pwd $PWD
