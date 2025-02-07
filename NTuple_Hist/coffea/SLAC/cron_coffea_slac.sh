#! /bin/bash

ssh iana "
cd /sdf/data/atlas/u/selbor/AF-Benchmarking/NTuple_Hist/coffea/SLAC/

srun run_example.sh
"
