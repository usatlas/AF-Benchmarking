#!/bin/bash


cd /global/homes/s/selbor/parsing_jobs

source bin/activate

python3 coffea_parsing.py
python3 truth3_el_parsing.py
python3 truth3_centos_parsing.py
python3 evnt_el_parsing.py
python3 evnt_centos_parsing.py
python3 rucio_parsing.py

deactivate
