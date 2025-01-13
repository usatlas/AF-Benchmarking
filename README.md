# AF Benchmarking

Contains benchmarking scripts used at the Tier 3 Analysis Facilities; UChicago, SLAC, and BNL. It also contains scripts used at NERSC.


## Types of jobs:

The jobs used for benchmarking are the of the following type:

- EVNT Generation
- TRUTH3
- Rucio Downloads
- NTuple-to-Histogram

Said jobs can either run interactively or in the batch system.

## Batch System

### UChicago
To execute jobs within the batch system you'll need both a submission file and a executable file. The submission file will give the batch system information about your job; where the job script is located and the requested resources. The executable file will contain the code we want the host to run; your code.

Consider the example below:

*TRUTH3 Executable File*
```bash
#!/bin/bash

# Input files are stored here
# Input/large files should always be stored in the /data/$USER directory
inputFile_dir="/data/$(whoami)/TRUTH3_Native_input_file/"

mkdir -p ${config_dir}

cp ~/AF-Benchmarking/TRUTH3/EVNT.root ${config_dir}

# Sets up our environment
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

# Sets the Athena version we want
asetup Athena,24.0.53,here
Derivation_tf.py --CA True --inputEVNTFile ${config_dir}EVNT.root --outputDAODFile=TRUTH3.root --formats TRUTH3

# Obtains and appends the host machine and payload size to the log file
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

