#! /bin/bash

# Setting up authorization for the download
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
lsetup emi
# Provides my pass phrase to voms
cat $HOME/pass.txt | voms-proxy-init -voms atlas
# Setting up rucio for our session
lsetup "rucio -w"

# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

# Conditional block determines the AF
# If the directory exists run the commands in the block
if [[ -d /sdf ]]; then
  user_name=$USER
  first_letter=${user_name:0:1}
  job_dir="/sdf/scratch/users/$first_letter/$USER/RucioJob"
  output_dir="/sdf/home/s/selbor/benchmarks/$curr_time/Rucio/"
elif [[ -d /usatlas ]]
then
  job_dir="/atlasgpfs01/usatlas/scratch/$USER/RucioJob"
  output_dir="/atlasgpfs01/usatlas/data/$USER/benchmarks/$curr_time/Rucio"
elif [[ -d /data ]]
then
  job_dir="/tmp/$USER/RucioJob"
  output_dir="/data/$USER/benchmarks/$curr_time/Rucio/"
elif [[-d /pscratch ]]
then
  user_name=$USER
  first_letter=${user_name:0:1}
  job_dir="/pscratch/sd/$first_letter/$USER/RucioJob/"
  output_dir="/global/homes/$first_letter/$USER/benchmarks/$curr_time/Rucio"
fi

# Makes the dir for the log file (if it doesn't exist)
mkdir -p ${output_dir}
# Goes into the newly created directory
cd ${job_dir}

# Remove the directory with the files, assuming it exists
download_ID="mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6491"

rm -r $download_ID/
# Begins the download
## The new data set will be mc23_13p6TeV:mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6491
rucio download --rses AGLT2_LOCALGROUPDISK $download_ID  2>&1 | tee $output_dir/rucio.log

# Gets and appends the host machine's name to the log file
hostname >> $output_dir/rucio.log
# Gets and appends the download size to the log file
du $download_ID/ >> $output_dir/rucio.log
