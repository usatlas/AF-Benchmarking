#! /bin/bash

ssh iana "
cd /sdf/scratch/atlas/selbor/Ntuple_Hist/event-loop-standard/
sbatch /sdf/home/s/selbor/AF-Benchmarking/NTuple_Hist/event_loop/SLAC/standard/event_loop_noarrays.sh
"
