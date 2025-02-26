#!/bin/bash

config_dir="EVNTFiles/100xxx/100001/"
user_name=$USER
first_letter=${user_name:0:1}

# Copies input files dir to the working dir
cp -r /sdf/home/$first_letter/$USER/AF-Benchmarking/EVNT/EVNTFiles .

# Appends time before Gen_tf.py to log file
echo $(date +"%H:%M:%S") >> split.log

asetup AthGeneration,23.6.31,here

export LHAPATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current:/cvmfs/atlas.cern.ch/repo/sw/software/23.6/sw/lcg/releases/LCG_104d_ATLAS_13/MCGenerators/lhapdf/6.5.3/x86_64-centos7-gcc11-opt/share/LHAPDF:/cvmfs/atlas.cern.ch/repo/sw/Generators/lhapdfsets/current

export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current:/cvmfs/atlas.cern.ch/repo/sw/software/23.6/sw/lcg/releases/LCG_104d_ATLAS_13/MCGenerators/lhapdf/6.5.3/x86_64-centos7-gcc11-opt/share/LHAPDF:/cvmfs/atlas.cern.ch/repo/sw/Generators/lhapdfsets/current

Gen_tf.py --ecmEnergy=13000.0 --jobConfig=${config_dir} --outputEVNTFile=EVNT.root --maxEvents=10000 --randomSeed=1001 2>&1 | tee pipe_file.log

# Appends time after Gen_tf.py to a log file
echo $(date +"%H:%M:%S") >> split.log

# Current time used for log file storage
curr_time=$(date +"%Y.%m.%dT%H")
# Defines the output directory
output_dir="/sdf/home/$first_letter/$USER/benchmarks/$curr_time/EVNT_container_centos"
# Creates the output directory
mkdir -p ${output_dir}
# Obtains and appends the host name and payload size to the log file
hostname >> split.log
du EVNT.root >> split.log

# Moves the log file and date_name file to the output directory
mv log.generate ${output_dir}
mv split.log ${output_dir}
mv pipe_file.log ${output_dir}
