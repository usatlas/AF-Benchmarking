#!/bin/bash

# Changes directory to $DATA/parsing_jobs
cd /data/selbor/parsing_jobs

# Runs the parsing scripts

python3 rucio_parsing.py

python3 evnt_native_parsing.py

python3 evnt_el_parsing.py

python3 evnt_centos_parsing.py

python3 truth3_centos_batch_parsing.py

python3 truth3_centos_interactive_parsing.py

python3 truth3_el_batch_parsing.py

python3 truth3_el_interactive_parsing.py

python3 truth3_native_batch_parsing.py

python3 truth3_native_interactive_parsing.py

