#!/bin/bash

# Prints the directory the job is started at
pwd 2>&1 | tee mwe.log

# Prints the items at the directory
ls >> mwe.log
