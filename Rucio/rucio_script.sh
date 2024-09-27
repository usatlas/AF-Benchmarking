#! /bin/bash

# Setting up authorization for the download
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
lsetup emi
echo "Wookiee13" | voms-proxy-init -voms atlas
lsetup "rucio -w"

# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Conditional block determines the AF
if [[ -d /sdf ]]; then
  job_dir="/sdf/scratch/users/s/selbor/RucioJob"
  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/Rucio/"
elif [[ -d /usatlas ]]
then
  job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/RucioJob"
  output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/Rucio"
elif [[ -d /data ]]
then 
  job_dir="/tmp/selbor/RucioJob"
  output_dir="/data/$USER/benchmarks/$curr_time/Rucio/"
fi

# Makes the dir for the log file (if it doesn't exist)
mkdir -p ${output_dir}
cd ${job_dir}
rm -r mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00/
# Begins the download
rucio download --rses AGLT2_LOCALGROUPDISK mc23_13p6TeV:mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00 2>&1 | tee $output_dir/rucio.log

# Gets the host name
hostname >> $output_dir/rucio.log
# Gets the download size
du mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00/ >> $output_dir/rucio.log
