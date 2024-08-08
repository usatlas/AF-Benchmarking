# AF Benchmarking

Contains scripts used at the AF for benchmarking. The jobs run every six hours with the aid of crontabs.

## Types of jobs:
The jobs used to benchmark run either interactively or as batch jobs.

Batch Jobs:
- EVNT Generation
- TRUTH3
- TRUTH3 within a CentOS7 container

Interactive Jobs:
- Rucio Downloads
- TRUTH3 within a CentOS7 container

## Cron-Jobs:
The scripts for each job are accessed by a crontab file. This runs the jobs every six hours. Below is the crontab file used at the UChicago AF:
``` bash
0 */6 * * * /home/selbor/benchmarks/Rucio/script_rucio.sh

0 */6 * * * /home/selbor/benchmarks/TRUTH3/script_TRUTH.sh

0 */6 * * * /home/selbor/benchmarks/EVNT/script_EVNT.sh

0 */6 * * * /home/selbor/benchmarks/TRUTH3_centos7/script_TRUTH3_centos.sh

0 */6 * * * /home/selbor/benchmarks/TRUTH3_centos7/to_run_centos_interactive.sh
```
