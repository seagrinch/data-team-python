#!/bin/bash
# Script to load Daily Statistics from Friedrich into database

# source activate datateam
date
cd /home/sage/data-team-python
./load-dailystats.py -s production -d /home/knuth/ooi_stats/stats/output/
