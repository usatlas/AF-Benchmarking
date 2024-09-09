#! /bin/bash

rm -r mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00/

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
lsetup emi
echo "Wookiee13" | voms-proxy-init -voms atlas

lsetup "rucio -w"

curr_time=$(date +"%Y.%m.%dT%H")

if [[ -d /sdf ]]; then
  output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/Rucio/"
elif [[ -d /usatlas ]]
then
  output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/Rucio"
elif [[ -d /data ]]
then 
  output_dir="/data/$USER/benchmarks/$curr_time/Rucio/"
fi

mkdir -p ${output_dir}

rucio download --rses AGLT2_LOCALGROUPDISK mc23_13p6TeV:mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00 2>&1 | tee $output_dir/rucio.log

hostname >> $output_dir/rucio.log
du mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00/ >> $output_dir/rucio.log
