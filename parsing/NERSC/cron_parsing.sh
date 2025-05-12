#!/bin/bash


cd /global/homes/s/selbor/parsing_jobs

source bin/activate

cd truth3_el/

python3 truth3_el_parsing.py

cd ../truth3_el_int/

python3 truth3_el_int_parsing.py

cd ../truth3_centos/

python3 truth3_centos_parsing.py

cd ../truth3_centos_int/

python3 truth3_centos_int_parsing.py

cd ../evnt_el/

python3 evnt_el_parsing.py

cd ../evnt_centos/

python3 evnt_centos_parsing.py

cd ../rucio_download/

python3 rucio_parsing.py

cd ../ntuple_coffea/

python3 coffea_parsing.py

cd -

deactivate
