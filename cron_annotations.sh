#!/bin/bash
# Script to load uFrame Annotations into the database

# source activate datateam
date
cd /home/sage/data-team-python
./load-annotations.py -s production 
