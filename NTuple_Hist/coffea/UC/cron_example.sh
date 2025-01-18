#!/bin/bash

cd /data/$(whoami)/ntuple_parse/env/

source bin/activate

python3 ntuple_coffea_parsing_script.py

deactivate
