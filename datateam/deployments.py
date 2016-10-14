""" OOI Data Team Import Module - Deployment Functions """
import csv
import time
from .common import *
import openpyxl as xl
import re
import glob

def find_deployment(db,reference_designator,deployment_number):
  """Find a deployment by reference_designator and deployment_number"""
  sql = 'reference_designator="%s" AND deployment_number="%s"' % (reference_designator, deployment_number)
  result = db.select('deployments',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save_deployment(db,data):
  """Save an deployment to the database"""
  id = find_deployment(db,data['reference_designator'],data['deployment_number'])
  if id == False:
    res = db.insert('deployments', data)
    print "Created deployment: " +data['reference_designator'] +' deployment #' +str(data['deployment_number'])
  else:
    res = db.update('deployments', id, data)
    print "Updated deployment: " +data['reference_designator'] +' deployment #' +str(data['deployment_number'])


def get_deployment(db,reference_designator,deployment_number):
  """Get a deployment by reference_designator and deployment_number"""
  sql = 'reference_designator="%s" AND deployment_number="%s"' % (reference_designator,deployment_number)
  result = db.select('deployments',sql)
  if len(result) > 0:
    return result[0]
  else:
    return False


def load(db):
  """Load deployments into the database"""
  r = db.truncate_table('deployments')
  print "Truncated deployments table"

  # Allowed columns
  columns = ['deploy_cuid','deployed_by','recover_cuid','recovered_by',
    'reference_designator','deployment_number',
    'version_number','start_date','stop_date','mooring_uid','node_uid','sensor_uid',
    'latitude','longitude','orbit','deployment_depth','water_depth','notes'
  ]

  # Read in deployment data
  file_mask = "repos/asset-management/deployment/*.csv"
  file_list = glob.glob(file_mask)

  for ifile in file_list:
    with open(ifile, 'rb') as csvfile:
      print "Loading file: " + ifile
      reader = csv.DictReader(csvfile)
      for row in reader:
        row['deploy_cuid'] = row['CUID_Deploy']
        row['deployed_by'] = row['deployedBy']
        row['recover_cuid'] = row['CUID_Recover']
        row['recovered_by'] = row['recoveredBy']
        row['reference_designator'] = row['Reference Designator']
        row['deployment_number'] = row['deploymentNumber']
        row['version_number'] = row['versionNumber']
        row['start_date'] = row['startDateTime']
        row['stop_date'] = row['stopDateTime']
        row['mooring_uid'] = row['mooring.uid']
        row['node_uid'] = row['node.uid']
        row['sensor_uid'] = row['sensor.uid']
        row['latitude'] = row['lat']
        row['longitude'] = row['lon']

        data = remove_extraneous_columns(columns, row)
        save_deployment(db,data)
