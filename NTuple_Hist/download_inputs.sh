#!/bin/bash

# ATLAS env
asetupATLAS

# Setting up rucio
lsetup rucio

# Downloading the input files
rucio download --rses MWT2_UC_LOCALGROUPDISK user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root

rucio download --rses MWT2_UC_LOCALGROUPDISK user.bhodkins.700402.Wmunugamma.mc20a.v2.1_ANALYSIS.root

rucio download --rses MWT2_UC_LOCALGROUPDISK user.bhodkins.700402.Wmunugamma.mc20d.v2.1_ANALYSIS.root
