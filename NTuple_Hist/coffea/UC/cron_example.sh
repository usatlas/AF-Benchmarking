#!/bin/bash

source /data/selbor/ntuple_parse/env/bin/activate

cd /data/selbor/parsing_jobs

python3 ntuple_coffea/ntuple_coffea.py

deactivate
