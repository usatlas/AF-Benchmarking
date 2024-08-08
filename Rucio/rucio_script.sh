#! /bin/bash

rm -r mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00/

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
lsetup emi
echo "Wookiee13" | voms-proxy-init -voms atlas

lsetup "rucio -w"


curr_time=$(date +"%Y.%m.%dT%H.%M.%S")

rucio download --rses AGLT2_LOCALGROUPDISK mc23_13p6TeV:mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6026_tid37222410_00 2>&1 | tee /data/selbor/Rucio/$curr_time.log
