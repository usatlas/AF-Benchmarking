#!/bin/bash


cd /global/homes/s/selbor/parsing_jobs || exit

source bin/activate

cd truth3_el/ || exit

python3 truth3_el_parsing.py

cd ../truth3_el_int/ || exit

python3 truth3_el_int_parsing.py

cd ../truth3_centos/ || exit

python3 truth3_centos_parsing.py

cd ../truth3_centos_int/ || exit

python3 truth3_centos_int_parsing.py

cd ../evnt_el/ || exit

python3 evnt_el_parsing.py

cd ../evnt_centos/ || exit

python3 evnt_centos_parsing.py

cd ../rucio_download/ || exit

python3 rucio_parsing.py

cd ../ntuple_coffea/ || exit

python3 coffea_parsing.py

cd - || exit

deactivate
