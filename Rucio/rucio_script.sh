#! /bin/bash

container_el9 (){ 
  # Takes the following parameters:
  # - job_dir (1)
  # - dir_mount (2)
  # - output_dir (3)
  # - download_ID (4)
  cd ${1}
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  export ALRB_localConfigDir=$HOME/localConfig
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -m ${2} -r "export RUCIO_ACCOUNT=jroblesg && \
    lsetup rucio &&\
    cat /srv/pass.txt | voms-proxy-init -voms atlas && \
    mkdir -p ${3} &&\
    rm -r ${4}/ &&\
    rucio download --rses AGLT2_LOCALGROUPDISK ${4}  2>&1 | tee rucio.log &&\
    hostname >> rucio.log &&\
    du ${4}/ >> rucio.log &&\
    mv rucio.log ${3}"
}

native_el9 () {
  # Takes the following parameters:
  # - output_dir
  # - job_dir
  # - download_ID
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  export ALRB_localConfigDir=$HOME/localConfig
  source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  lsetup emi
  cat $HOME/pass.txt | voms-proxy-init -voms atlas
  lsetup "rucio -w"
  mkdir -p ${1}
  cd ${2}
  rm -r ${3}/
  rucio download --rses AGLT2_LOCALGROUPDISK ${3}  2>&1 | tee rucio.log
  hostname >> rucio.log
  du ${3}/ >> rucio.log
  mv rucio.log ${1}
}

# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")
download_ID="mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6491"
# Conditional block determines the AF
# If the directory exists run the commands in the block
if [[ -d /sdf ]]; then
  user_name=$USER
  first_letter=${user_name:0:1}
  job_dir="/sdf/scratch/atlas/$user_name/RucioJob"
  dir_mount="/sdf/data/atlas/u/selbor/benchmarks/"
  output_dir="/sdf/data/atlas/u/selbor/benchmarks/$curr_time/Rucio/"
  container_el9 ${job_dir} ${dir_mount} ${output_dir} ${download_ID}
elif [[ -d /usatlas ]]
then
  job_dir="/atlasgpfs01/usatlas/scratch/jroblesgo/Rucio/"
  dir_mount="/atlasgpfs01/usatlas/data/"
  output_dir="/atlasgpfs01/usatlas/data/jroblesgo/benchmarks/$curr_time/Rucio"
  container_el9 ${job_dir} ${dir_mount} ${output_dir} ${download_ID}
elif [[ -d /data ]]
then
  job_dir="/data/$USER/RucioJob"
  output_dir="/data/$USER/benchmarks/$curr_time/Rucio/"
  native_el9 ${output_dir} ${job_dir} ${download_ID}
elif [[ -d /pscratch ]]
then
  user_name=$USER
  first_letter=${user_name:0:1}
  job_dir="/pscratch/sd/s/selbor/Rucio/"
  dir_mount="/global/cfs/cdirs/m2616/selbor/benchmarks/"
  output_dir="/global/cfs/cdirs/m2616/selbor/benchmarks/$curr_time/Rucio"
  container_el9 ${job_dir} ${dir_mount} ${output_dir} ${download_ID}
fi


