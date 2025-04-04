#!/bin/bash

ssh iana "
cd /sdf/home/s/selbor/TRUTH3_int/el

rm -r *

~/AF-Benchmarking/TRUTH3/SLAC/run_truth3_el9_interactive.sh"
