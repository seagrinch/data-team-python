""" OOI Data Team Import Module - Import Reviews """
import csv
from .common import *
import fnmatch
import os
import pandas as pd
import datetime
import time


def find_review(db,reference_designator,deployment,stream):
  """Find a Review record"""
  sql = 'reference_designator="%s" AND deployment="%s" AND stream="%s"' % (reference_designator, deployment, stream)
  result = db.select('reviews',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save_review(db,data):
  """Save a Review to the database"""
  id = find_review(db,data['reference_designator'],data['deployment'],data['stream'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('reviews', data)
    print "Created Review: " + data['reference_designator'] + ' ' + str(data['deployment']) + ' ' + str(data['stream'])
  else:
    #data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('reviews', id, data)
    print "Updated Review: " + data['reference_designator'] + ' ' + str(data['deployment']) + ' ' + str(data['stream'])


def get_review(db,reference_designator,deployment,stream):
  """Get a Review record"""
  sql = 'reference_designator="%s" AND deployment="%s" AND stream="%s"' % (reference_designator, deployment, stream)
  result = db.select('reviews',sql)
  if len(result) > 0:
    return result[0]
  else:
    return False

def load(db):
  """Load Reviews into the database"""
  
  # Allowed columns
  columns = ['reference_designator','deployment','preferred_method','stream',
  'start_days_missing','end_days_missing','location_diff_km',
  'n_days_deployed','n_timestamps','n_days','deploy_depth','pressure_mean','pressure_diff','sampling_rate_seconds',
  'gaps_num','gaps_num_days','timestamp_test','n_science_vars','valid_data_test',
  'variable_comparison_test','full_dataset_test','coordinate_test','file_downloaded','status']

  # Find summary files
  file_mask = "repos/data-review-tools/data_review/output/"
  file_list = []
  for root, dirnames, filenames in os.walk(file_mask):
    for filename in fnmatch.filter(filenames, '*_file_summary.csv'):
      file_list.append(os.path.join(root, filename))
  
  # Read in Ingestion data
  for ifile in file_list:
    print "Loading file: " + ifile
    with open(ifile, 'rb') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        row['reference_designator'] = ifile.split('/')[-1][0:27]
        row['deployment'] = int(row['deployment'][-3:])
        review = get_review(db,row['reference_designator'],row['deployment'],row['stream'])
        if (review['status'] == None):
          row['status'] = 'Tested'
        data = remove_extraneous_columns(columns, row)
        save_review(db,data)


def find_deployments(db,reference_designator):
  """Find deployments by reference_designator"""
  sql = 'reference_designator="%s"' % (reference_designator)
  result = db.select('deployments',sql)
  if len(result) > 0:
    return result
  else:
    return False


def yes_no(question):
    """Prompt user with a yes/no question"""
    yes = set(['yes'])
    no = set(['no','n'])
    
    while True:
        choice = raw_input(question).lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           print "Please respond with 'yes' or 'no'\n"


def load_baseline(db):
  """Load Review Baseline into the database"""

  baseline = pd.read_csv("infrastructure/stream_review_baseline.csv")
  columns = ['reference_designator', 'deployment', 'preferred_method', 'stream']
  for index, row in baseline.iterrows():
    row = row.to_dict()
    row['preferred_method'] = row['method']
    # print(row['reference_designator'])
    deployments = find_deployments(db,row['reference_designator'])
    for d in deployments:
      # print(str(d['deployment_number']) + str(d['stop_date']))
      if(d['stop_date'] is not None and d['stop_date'] < datetime.datetime(2018, 10, 1)):
        row['deployment'] = d['deployment_number']
        data = remove_extraneous_columns(columns, row)
        save_review(db, data)
      #  print('Good' + str(d['deployment_number']) + " " + d['stop_date'].strftime("%y-%m-%d"))
      #else:
      #  if(d['stop_date'] is None):
      #    print('Bad' + str(d['deployment_number']))
      #  else: 
      #    print('Bad' + str(d['deployment_number']) + " " + d['stop_date'].strftime("%y-%m-%d"))

  # One time update of Instrument Status
  pyanswer = yes_no('Overwrite Instrument Status? ')
  if(pyanswer):
    instruments = baseline['reference_designator'].unique()
    columns = ['reference_designator', 'current_status']
    from datateam import designators
    for inst in instruments:
      data={}
      data['reference_designator'] = inst
      data['current_status'] = 'Todo'
      designators.save(db, 'instruments', data, columns)

