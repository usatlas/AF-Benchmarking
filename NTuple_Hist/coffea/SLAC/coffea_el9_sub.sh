#!/bin/bash
#
#SBATCH --account=atlas:usatlas
#SBATCH --partition=ampere
#SBATCH --gpus a100:0
#SBATCH --job-name=coffea_el9
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=16g
#SBATCH --time=0-01:00:00


unset KRB5CCNAME

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase 

# Use ALRB_CONT_CMDOPTS to provide bind mount, etc. options 

export ALRB_CONT_CMDOPTS="-B /sdf"

export ALRB_CONT_RUNPAYLOAD="source /sdf/home/s/$USER/AF-Benchmarking/NTuple_Hist/coffea/SLAC/run_example.sh"

source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -c el9 -m /sdf/data/atlas/


