#!/bin/bash
#
#SBATCH --account=atlas:usatlas
#SBATCH --partition=ampere
#SBATCH --gpus a100:0
#SBATCH --job-name=evnt_batch_centos7
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=4g
#SBATCH --time=0-02:00:00


unset KRB5CCNAME

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase 

# Use ALRB_CONT_CMDOPTS to provide bind mount, etc. options 

export ALRB_CONT_CMDOPTS="-B /sdf"

export ALRB_CONT_RUNPAYLOAD="source /sdf/data/atlas/u/$USER/AF-Benchmarking/EVNT/SLAC/run_evnt_centos_container.sh"

source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -c centos7
