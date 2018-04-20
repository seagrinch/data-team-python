#!/bin/bash
# This script updates the preload-database git repot
# And then updates the sqlite database based on the latest data
# Before running, don't forget to change the conda or python environment 
# For example: workon preload

cd repos/preload-database
./load_preload.py
rm preload.db
sqlite3 preload.db < preload_database.sql

# Old script
#!/usr/bin/env python
# import database
# if __name__ == '__main__':
#   database_util.generate_preload_database_from_script()
