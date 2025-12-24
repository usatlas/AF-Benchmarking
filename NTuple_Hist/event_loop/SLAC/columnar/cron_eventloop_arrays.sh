#! /bin/bash

ssh iana "
cd /sdf/scratch/atlas/selbor/Ntuple_Hist/event-loop-columnar/
sbatch /sdf/home/s/selbor/AF-Benchmarking/NTuple_Hist/event_loop/SLAC/columnar/event_loop_arrays.sh
"
