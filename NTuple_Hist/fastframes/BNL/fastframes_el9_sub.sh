# shellcheck shell=bash disable=all
Universe = vanilla


Output = /usatlas/u/jroblesgo/batch_output_files/fastframes/myjob.$(Cluster).$(Process).out
Error = /usatlas/u/jroblesgo/batch_output_files/fastframes/myjob.$(Cluster).$(Process).err
Log = /usatlas/u/jroblesgo/batch_output_files/fastframes/myjob.$(Cluster).$(Process).log

Executable = /usatlas/u/jroblesgo/AF-Benchmarking/NTuple_Hist/fastframes/BNL/run_fastframes.sh

request_memory = 3GB
request_cpus = 1

Queue 1
