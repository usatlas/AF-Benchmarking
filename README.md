# AF Benchmarking

Contains benchmarking scripts used at the Tier 3 Analysis Facilities:
- [UChicago](https://github.com/usatlas/AF-Benchmarking?tab=readme-ov-file#uchicago)
- [SLAC](https://github.com/usatlas/AF-Benchmarking#slac)
- [BNL](https://github.com/usatlas/AF-Benchmarking#bnl)

It now contains scripts used at NERSC.

The jobs used for benchmarking are the of the following type:

- EVNT Generation
- TRUTH3
- Rucio Downloads
- NTuple-to-Histogram

Said jobs can either run interactively or in the batch system.

For more information on the Tier 3 AFs check out the read-the-docs page, [here](https://usatlas.readthedocs.io/projects/af-docs/en/latest/).

## Batch System
To execute jobs within the batch system you'll need both a submission file and a executable file. The submission file will give the batch system information about your job; where the job script is located and the requested resources. The executable file will contain the code we want the host to run; your code. Below you can find examples to help you get started at the Tier 3 AFs.

The following sections display submission and executable files that can be used at the respective analysis facilities.

### UChicago

*TRUTH3 Executable File*
```bash
#!/bin/bash

# Input/large files should be stored in the /data/$USER directory
# Change <username> to your username
inputFile_dir="/data/<username>/TRUTH3_Native_input_file/"

# Creates the file directory
mkdir -p ${inputFile_dir}

# Moves input files to the input file directory
cp ~/AF-Benchmarking/TRUTH3/EVNT.root ${inputFile_dir}

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${inputFile_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Obtains and appends the host machine to the log file
hostname >> log.Derivation

```

*TRUTH3 Submission File*
```bash
Universe = vanilla


Output = example_truth3_native.$(Cluster).$(Process).out
Error = example_truth3_native.$(Cluster).$(Process).err
Log = example_truth3_native.$(Cluster).$(Process).log

# Path to your job script, in this case 
# Change <username> to your own username
Executable = /home/<username>/AF-Benchmarking/TRUTH3/UC/example_run_truth3_native_batch.sh

request_memory = 3GB
request_cpus = 1

Queue 1
```

### SLAC

When working at SLAC, the jobs submitted must be containerized. The example below outlines how to do this using a TRUTH3 job running in EL9 container.

*TRUTH3 Executable File*

```bash
#!/bin/bash

# Defines the OS wanted for the container
OScontainer="el9"

# Initializes the container with the OS defined in the previous line
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c ${OScontainer} -r "cp -r /home/$USER/TRUTH3Files/ . && \
asetup Athena,24.0.53,here && \
Derivation_tf.py --CA True --inputEVNTFile /srv/TRUTH3Files/el9/EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

# Appends the host-name to the end of the log file
hostname >> log.Derivation
```
*TRUTH3 Submission File*

```bash
#!/bin/bash
#
#SBATCH --account=atlas:usatlas
#SBATCH --partition=ampere
#SBATCH --gpus a100:0
#SBATCH --job-name=truth3_batch
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=4g
#SBATCH --time=0-00:30:00

unset KRB5CCNAME

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase 

# Use ALRB_CONT_CMDOPTS to provide bind mount, etc. options 

export ALRB_CONT_CMDOPTS="-B /sdf"

export ALRB_CONT_RUNPAYLOAD="source $HOME/AF-Benchmarking/TRUTH3/SLAC/run_truth3_el9_container.sh"

source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -c el9
```

### BNL

*TRUTH3 Executable File*

```bash
#!/bin/bash

# Config Dir Needed
config_dir="TRUTH3Files/"

# Sets up the environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase

# Sets up the container:
## -c : used to make a container followed by the OS we want to use
## -m : mounts a specific directory
## -r : precedes the commands we want to run within the container
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c el9 -r "asetup Athena,24.0.53,here && \
  Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT_el9_batch.root --outputDAODFile=TRUTH3.root --formats TRUTH3"

# Current time used for file storage
curr_time=$(date +"%Y.%m.%dT%H")

# Defines the output directory
output_dir="/atlasgpfs01/usatlas/data/${USER}/benchmarks/$curr_time/TRUTH3_el9_batch"

# Creates the output directory
mkdir -p ${output_dir}

# Obtains and appends the host name and payload size to the log file
hostname >> log.Derivation
du DAOD_TRUTH3.TRUTH3.root >> log.Derivation

# Moves the log file to the output directory
mv log.Derivation ${output_dir}
```

*TRUTH3 Submission File*

```bash
Universe = vanilla


Output = /atlasgpfs01/usatlas/data/<username>/myjob.$(Cluster).$(Process).out
Error = /atlasgpfs01/usatlas/data/<username>/myjob.$(Cluster).$(Process).err
Log = /atlasgpfs01/usatlas/data/<username>/myjob.$(Cluster).$(Process).log

Executable = /usatlas/u/<username>/AF-Benchmarking/TRUTH3/BNL/run_truth3_el9_batch.sh

request_memory = 3GB
request_cpus = 1

Queue 1
```

