#!/usr/bin/env python
# OOI Datateam Import - Script to Import Data Annotations

import datateam
import argparse
import glob
import csv
import os
import dateutil.parser

# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal - Annotation Importer')
parser.add_argument('-s','--server',
  choices=['production','development'],
  default='development',
  help='Database server')
args = parser.parse_args()


# Allowed columns
columns = ['reference_designator', 'deployment','method','stream','parameter',
  'start_datetime','end_datetime','annotation','status',
  'redmine_issue','todo','reviewed_by','reviewed_date']

def save(db, data):
  """Save annotation to the database"""
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
  if s:
    v = dateutil.parser.parse(s)
    return v.strftime('%Y-%m-%d %H:%M:%S')
  else:
    return None
# Old version
#   if s.endswith('Z'):
#     return s[:-1]
#   else:
#     return s


def process_row(row,reference_designator,method='',stream='',parameter=''):
  row['reference_designator'] = reference_designator.strip()
  row['method'] = method
  row['stream'] = stream
  row['parameter'] = parameter
  row['deployment'] = convert_deployment(row['Deployment'])
  row['start_datetime'] = fix_time(row['StartTime'])
  row['end_datetime'] = fix_time(row['EndTime'])
  row['annotation'] = row['Annotation'].decode('utf-8', errors='replace')
  row['status'] = row['Status']
  row['redmine_issue'] = row['Redmine#']
  row['todo'] = row['Todo']
  row['reviewed_by'] = row['ReviewedBy'] if 'ReviewedBy' in row else ''
  row['reviewed_date'] = fix_time(row['ReviewedDate']) if 'ReviewedDate' in row else ''
  #  print '%s - %s' % (row['reviewed_date'],fix_time(row['reviewed_date']))


def load_annotations(db):
  """Load Annotations"""
  r = db.truncate_table('annotations')
  print "Truncated annotations table"

  file_mask = "repos/annotations/annotations/*"
  site_list = glob.glob(file_mask)
  for site_directory in site_list:
    # First, process the Site Annotation file
    site_csv_list = glob.glob(site_directory + '/*.csv')
    for ifile in site_csv_list:
      print "Loading: " + ifile
      with open(ifile, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
          process_row(row,row['Level'])
          save(db,row)
    # Second, process the Instrument Directories, and the Stream files in them
    subdir_list = glob.glob(site_directory+'/*/')
    for subdirectory in subdir_list:
      stream_csv_list = glob.glob(subdirectory + '/*.csv')
      for ifile in stream_csv_list:
        print "Loading: " + ifile
        rd = os.path.dirname(ifile).split('/')[-1]
        method = os.path.basename(ifile).split('-')[0]
        stream = os.path.basename(ifile).split('-')[1].split('.')[0].replace('_parameters','')
        with open(ifile, 'rb') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
            if 'Status' in row and row['Status']:
              if os.path.basename(ifile).find('parameters')>0:
                process_row(row,rd,method,stream,row['Level'])
                save(db,row)
              else:
                process_row(row,rd,method,stream)
                save(db,row)


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config(args.server)
  load_annotations(db)


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
