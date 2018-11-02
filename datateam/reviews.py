""" OOI Data Team Import Module - Import Reviews """
import csv
from .common import *
import fnmatch
import os


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
    res = db.insert('reviews', data)
    print "Created Review: " + data['reference_designator'] + ' ' + str(data['deployment']) + ' ' + str(data['stream'])
  else:
    res = db.update('reviews', id, data)
    print "Updated Review: " + data['reference_designator'] + ' ' + str(data['deployment']) + ' ' + str(data['stream'])


def load(db):
  """Load Reviews into the database"""
  
  # Allowed columns
  columns = ['reference_designator','deployment','preferred_method','stream',
  'start_days_missing','end_days_missing','location_diff_km',
  'n_days_deployed','n_timestamps','n_days','deploy_depth','pressure_mean','pressure_diff',
  'gaps_num','gaps_num_days','timestamp_test','n_science_vars','valid_data_test',
  'variable_comparison_test','full_dataset_test','coordinate_test','file_downloaded']

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
        data = remove_extraneous_columns(columns, row)
        save_review(db,data)
