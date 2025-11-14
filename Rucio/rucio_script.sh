#! /bin/bash

# Gets the current time
curr_time=$(date +"%Y.%m.%dT%H")

download_ID="mc23_13p6TeV.700866.Sh_2214_WWW_3l3v_EW6.deriv.DAOD_PHYSLITE.e8532_e8528_s4162_s4114_r14622_r14663_p6491"

container_el9 (){
  # Takes the following parameters:
  # - job_dir (1)
  # - dir_mount (2)
  # - output_dir (3)
  # - download_ID (4)
  cd "${1}" || exit
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  export ALRB_localConfigDir="$HOME"/localConfig
# shellcheck disable=SC1091
# shellcheck disable=SC2115
  source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh -c el9 -m "${2}" -r "export RUCIO_ACCOUNT=jroblesg && \
    lsetup rucio &&\
    cat /srv/pass.txt | voms-proxy-init -voms atlas && \
    mkdir -p \"${3}\" &&\
    rm -r \"${4:?}\"/ &&\
    rucio download --rses AGLT2_LOCALGROUPDISK \"${4}\"  2>&1 | tee rucio.log &&\
    hostname >> rucio.log &&\
    du \"${4}\"/ >> rucio.log &&\
    mv rucio.log \"${3}\""
}

native_el9 () {
  # Takes the following parameters:
  # - output_dir
  # - job_dir
  # - download_ID
  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  export ALRB_localConfigDir="$HOME"/localConfig
# shellcheck disable=SC1091
  source "${ATLAS_LOCAL_ROOT_BASE}"/user/atlasLocalSetup.sh
  lsetup emi
  cat "$HOME"/pass.txt | voms-proxy-init -voms atlas
  lsetup "rucio -w"
  mkdir -p "${1}"
  cd "${2}" || exit
  # shellcheck disable=SC2115
  rm -r "${3:?}"/
  rucio download --rses AGLT2_LOCALGROUPDISK "${3}"  2>&1 | tee rucio.log
  hostname >> rucio.log
  du "${3}"/ >> rucio.log
  mv rucio.log "${1}"
}

# --- Determine site ---
# Conditional block determines the AF
# If the directory exists run the commands in the block
site="$1"
if [[ -z "$site" ]]; then
    # Auto-detect
    if [[ -d /sdf ]]; then
        site="slac"
    elif [[ -d /usatlas ]]; then
        site="uchicago"
    elif [[ -d /data ]]; then
        site="bnl"
    elif [[ -d /pscratch ]]; then
        site="nersc"
    else
        echo "Cannot detect site from directories"
        exit 1
    fi
fi
echo "Running for site: $site"

# --- Configure directories based on site ---
case "$site" in
    bnl)
        job_dir="$HOME/af_benchmarking/rucio/"
        dir_mount="/atlasgpfs01/usatlas/data/"
        output_dir="${job_dir}/${curr_time}/"
        container_el9 "$job_dir" "$dir_mount" "$output_dir" "$download_ID"
        ;;
    slac)
        job_dir="$HOME/af_benchmarking/rucio/"
        dir_mount="/sdf/data/atlas/u/selbor/benchmarks/"
        output_dir="${job_dir}/${curr_time}/"
        container_el9 "$job_dir" "$dir_mount" "$output_dir" "$download_ID"
        ;;
    uchicago)
        job_dir="$HOME/af_benchmarking/rucio/"
        output_dir="${job_dir}/${curr_time}/"
        native_el9 "$output_dir" "$job_dir" "$download_ID"
        ;;
    nersc)
        job_dir="$HOME/af_benchmarking/rucio/"
        dir_mount="/global/cfs/cdirs/m2616/selbor/benchmarks/"
        output_dir="${job_dir}/${curr_time}/"
        container_el9 "${job_dir}" "${dir_mount}" "${output_dir}" "${download_ID}"
        ;;
    *)
        echo "Unknown site: $site"
        exit 1
        ;;
esac

echo "Download complete. Output dir: $output_dir"
