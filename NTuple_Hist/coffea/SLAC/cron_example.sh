#!/bin/bash
ssh iana "
cd /sdf/home/s/selbor/parsing/env/

source bin/activate

python3 ntuple_coffea_parsing_script.py

deactivate
"
