#!/usr/bin/env python
# OOI Datateam Import - Script to Import Data Annotations

import datateam
import argparse
import glob
import csv

# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal - Annotation Importer')
parser.add_argument('-s','--server',
  choices=['production','development'],
  default='development',
  help='Database server')
args = parser.parse_args()


def save(db, data):
  """Save a stats record to the database"""

  # Allowed columns
  columns = ['reference_designator', 'deployment','method','stream','parameter',
    'start_datetime','end_datetime','annotation','status',
    'redmine_issue','todo','reviewed_by','reviewed_date']
  data = datateam.common.remove_extraneous_columns(columns, data)
  res = db.insert('annotations', data)
  print "Added: %s %s" % (data['reference_designator'], (data['start_datetime'] if 'start_datetime' in data else ''))

#   id = find(db,data['reference_designator'],data['month'])
#   if id == False:
#     #data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
#     res = db.insert('monthly_stats', data)
#     print "Created: " +data['reference_designator'] +' ' +data['month']
#   else:
#     #data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
#     res = db.update('monthly_stats', id, data)
#     #print "Updated: " +data['reference_designator'] +' ' +data['month']


def convert_deployment(s):
  if s.startswith('D'):
    s = s[1:]
    return int(s)
  elif s.isdigit(): 
    return int(s)
  else:
    return False

def fix_time(s):
  if s.endswith('Z'):
    return s[:-1]
  else:
    return s

def load_annotations(db):
  """Load Annotations"""
  r = db.truncate_table('annotations')
  print "Truncated annotations table"

  file_mask = "repos/annotations/annotations/*"
  directory_list = glob.glob(file_mask)

  for directory in directory_list:
    file_list = glob.glob(directory + '/*.csv')
    for ifile in file_list:
      with open(ifile, 'rb') as csvfile:
        print "Loading file: " + ifile
        reader = csv.DictReader(csvfile)
        for row in reader:
          row['reference_designator'] = row['Level']
          row['deployment'] = convert_deployment(row['Deployment'])
          row['start_datetime'] = fix_time(row['StartTime'])
          row['end_datetime'] = fix_time(row['EndTime'])
          row['annotation'] = row['Annotation']
          row['status'] = row['Status']
          row['redmine_issue'] = row['Redmine#']
          row['todo'] = row['Todo']
          row['reviewed_by'] = row['ReviewedBy'] if 'ReviewedBy' in row else ''
          row['reviewed_date'] = fix_time(row['ReviewedDate']) if 'ReviewedDate' in row else ''
#           print '%s - %s' % (row['reviewed_date'],fix_time(row['reviewed_date']))
          save(db,row)

#           row['class'] = directory.split('/')[-1]
#           row['asset_uid'] = ifile.split('/')[-1].split('__')[0]
#           row['start_date'] = ifile.split('/')[-1].split('__')[1].split('.')[0]


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config(args.server)
  load_annotations(db)


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
