#!/bin/bash

# Changes directory to $DATA/parsing_jobs
cd /data/selbor/parsing_jobs || exit || exit

# Runs the parsing scripts

python3 rucio_download/rucio_parsing.py

python3 evnt_native/evnt_native_parsing.py

python3 evnt_el/evnt_el_parsing.py

python3 evnt_centos/evnt_centos_parsing.py

python3 truth3_centos/truth3_centos_batch_parsing.py

python3 truth3_centos_int/truth3_centos_interactive_parsing.py

python3 truth3_el/truth3_el_batch_parsing.py

python3 truth3_el_int/truth3_el_interactive_parsing.py

python3 truth3_native/truth3_native_batch_parsing.py

python3 truth3_native_int/truth3_native_interactive_parsing.py

python3 ntuple_coffea/ntuple_coffea.py
