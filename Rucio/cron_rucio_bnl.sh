#! /bin/bash

# Directory where I want the job to run from
job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/RucioJob"

# Changes to desired directory
cd ${job_dir}

# IF the download exits it will remove it
rm -r mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6491/

# Calls the script that will trigger the job
~/AF-Benchmarking/Rucio/rucio_script.sh
