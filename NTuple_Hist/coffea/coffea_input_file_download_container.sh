#!/bin/bash

# File to use: user.bhodkins.42164748._000288.ANALYSIS.root

container_el9 (){ 
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  export ALRB_localConfigDir=$HOME/localConfig
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -r "export RUCIO_ACCOUNT=jroblesg && \
    lsetup rucio &&\
    cat /home/$USER/pass.txt | voms-proxy-init -voms atlas && \
    rucio download --rses MWT2_UC_LOCALGROUPDISK user.bhodkins:user.bhodkins.data2018_AllYear.v2.0_ANALYSIS.root"
}


container_el9
