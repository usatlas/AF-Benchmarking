#!/bin/bash

# ATLAS env
asetupATLAS

# Setting up rucio
lsetup rucio

# Downloading the input files
rucio download --rses MWT2_UC_LOCALGROUPDISK user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root
