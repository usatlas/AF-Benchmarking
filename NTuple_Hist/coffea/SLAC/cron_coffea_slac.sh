#! /bin/bash

ssh iana "
cd /sdf/scratch/atlas/selbor/Ntuple_Hist/coffea/
sbatch /sdf/home/s/selbor/AF-Benchmarking/NTuple_Hist/coffea/SLAC/coffea_el9_sub.sh
"
