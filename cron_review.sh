#!/bin/bash
# Script to load Data Team reviews into the database
# Written by Sage 12/11/18

# source activate datateam
date

# Switch to main directory
cd /home/sage/data-team-python

# Update git repos
cd repos/data-review-tools/
git pull
cd ../../

# Run database update scripts
./load-data.py -s production -o reviews

date
