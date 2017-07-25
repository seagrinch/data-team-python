""" OOI Data Team Import Module - Deployment Functions """
import csv
import time
from .common import *
import openpyxl as xl
import re
import glob


# Allowed columns
columns = ['deploy_cuid','deployed_by','recover_cuid','recovered_by',
  'reference_designator','deployment_number',
  'version_number','start_date','stop_date','mooring_uid','node_uid','sensor_uid',
  'latitude','longitude','orbit','deployment_depth','water_depth','notes'
]


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


# Initialize blank parents array
parents = []

def check_parent(db, row):
  """Create a parent record, and save if new"""
  # Create a parent item
  parent = {
    'deploy_cuid': row.get('deploy_cuid'),
    'deployed_by': row.get('deployed_by'),
    'recover_cuid': row.get('recover_cuid'),
    'recovered_by': row.get('recovered_by'),
    'deployment_number': row.get('deployment_number'),
    'start_date': row.get('start_date'),
    'stop_date': row.get('stop_date'),
    'latitude': row.get('latitude'),
    'longitude': row.get('longitude')
  }
  rd = row.get('reference_designator')
  if rd[0:2] == 'RS':
    parent['reference_designator'] = row['reference_designator'][0:14]
    parent['sensor_uid'] = row.get('mooring_uid')
  elif rd[4:8] == 'MOAS':
    parent['reference_designator'] = row['reference_designator'][0:14]
    parent['sensor_uid'] = row.get('node_uid')
  else: 
    parent['reference_designator'] = row['reference_designator'][0:8]
    parent['sensor_uid'] = row.get('mooring_uid')

  # Save Parent Site or Node Deployment first if not already saved
  parent_id = parent['reference_designator'] + '-' + parent['deployment_number']
  
  if parent_id not in parents:
    parent = remove_extraneous_columns(columns, parent)
    save_deployment(db,parent)
    parents.append(parent_id)


def load(db):
  """Load deployments into the database"""
  r = db.truncate_table('deployments')
  print "Truncated deployments table"

  # Read in deployment data
  file_mask = "repos/asset-management/deployment/*.csv"
  file_list = glob.glob(file_mask)

  for ifile in file_list:
    with open(ifile, 'rb') as csvfile:
      print "Loading file: " + ifile
      reader = csv.DictReader(csvfile)
      for row in reader:      
        # Tweak row entries to match database 
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

        row = remove_extraneous_columns(columns, row)

        # First, save parent deployment if new
        check_parent(db, row)
      
        # Save Instrument Deployment
        if len(row['reference_designator'])==27 or len(row['reference_designator'])==14 or len(row['reference_designator'])==8:
          if row.get('deploy_cuid','').startswith('#'):
            print "Ignored Deployment: " +row['reference_designator'] +' deployment #' +str(row['deployment_number'])
          else:
            save_deployment(db,row)
        else:
          print "Invalid Reference Designator: " +row['reference_designator'] +' deployment #' +str(row['deployment_number'])
