#!/bin/bash

# Blocks sets up rucio downloads
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir="$HOME"/localConfig
# shellcheck disable=SC1091
source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh
lsetup emi
cat "$HOME"/pass.txt | voms-proxy-init -voms atlas
lsetup "rucio -w"

# File to use: user.bhodkins.42164748._000288.ANALYSIS.root
rucio download --rses MWT2_UC_LOCALGROUPDISK user.bhodkins:user.bhodkins.data2018_AllYear.v2.0_ANALYSIS.root
