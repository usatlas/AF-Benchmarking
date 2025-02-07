#!/bin/bash
config_dir="EVNTFiles/100xxx/100001/"
cp -r /sdf/data/atlas/u/$USER/EVNTFiles .

asetup AthGeneration,23.6.31,here

export LHAPATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current:/cvmfs/atlas.cern.ch/repo/sw/software/23.6/sw/lcg/releases/LCG_104d_ATLAS_13/MCGenerators/lhapdf/6.5.3/x86_64-centos7-gcc11-opt/share/LHAPDF:/cvmfs/atlas.cern.ch/repo/sw/Generators/lhapdfsets/current

export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current:/cvmfs/atlas.cern.ch/repo/sw/software/23.6/sw/lcg/releases/LCG_104d_ATLAS_13/MCGenerators/lhapdf/6.5.3/x86_64-centos7-gcc11-opt/share/LHAPDF:/cvmfs/atlas.cern.ch/repo/sw/Generators/lhapdfsets/current

Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir} --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=1001


# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")
# Defines the output directory
output_dir="/sdf/data/atlas/u/$USER/benchmarks/$curr_time/EVNT_container_centos"
# Creates the output directory
mkdir -p ${output_dir}
# Obtains and appends the host name and payload size to the log file
hostname >> log.generate
du EVNT.root >> log.generate
# Moves the log file to the output directory
mv log.generate ${output_dir}
