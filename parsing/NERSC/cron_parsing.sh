#!/bin/bash


cd /global/homes/s/selbor/parsing_jobs

source bin/activate

python3 truth3_el/truth3_el_parsing.py
python3 truth3_el_int/truth3_el_int_parsing.py
python3 truth3_centos/truth3_centos_parsing.py
python3 truth3_centos_int/truth3_centos_int_parsing.py
python3 evnt_el/evnt_el_parsing.py
python3 evnt_centos/evnt_centos_parsing.py
python3 rucio_download/rucio_parsing.py
python3 coffea_parsing.py

deactivate
