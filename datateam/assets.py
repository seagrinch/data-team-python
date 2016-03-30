""" OOI Datateam Import Module - Asset Functions """
import csv
import time
from .common import *

def find(db,ooi_barcode):
  """Find an Asset by ooi_barcode"""
  sql = 'ooi_barcode="%s"' % ooi_barcode
  result = db.select('assets',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save an Asset to the database"""
  if data['OOI BARCODE'] and data['OOI BARCODE']!='Waiting for AT Number Assignment':
    newdata= {
      'ooi_barcode': data['OOI BARCODE'],
      'description_of_equipment': data['DESCRIPTION OF EQUIPMENT'],
      'quant': data['QUANT'],
      'manufacturer': data['Manufacturer'],
      'model': data['Model'],
      
      'manufacturer_serial_no': data["Manufacturer's Serial No./Other Identifier"],
      'firmware_version': data['Firmware Version'],
      'source_of_the_equipment': data['Source of the Equipment/Award No. or PO No.'],
      'whether_title': data['Whether Title Vests in Recipient or Federal Gov'],
      'location': data['LOCATION'],
      
      'room_number': data['ROOM NUMBER/CUSTODY'],
      'condition': data['COND.'],
      'acquisition_date': data['ACQUISITION DATE'],
      'original_cost': data['ORIGINAL COST'],
      'federal_participation': data['PERCENTAGE OF FEDERAL PARTICIPATION'],
      
      'comments': data['comments'],
      'primary_tag_date': data['primary_tag_date'],
      'primary_tag_organization': data['primary_tag_organization'],
      'primary_institute_asset_tag': data['primary_institute_asset_tag'],
      'secondary_tag_date': data['secondary_tag_date'],
      
      'second_tag_organization': data['second_tag_organization'],
      'institute_asset_tag': data['institute_asset_tag'],
      'doi_tag_date': data['doi_tag_date'],
      'doi_tag_organization': data['doi_tag_organization'],
      'doi_institute_asset_tag': data['doi_institute_asset_tag'],
      }
  
    columns = ['ooi_barcode', 'description_of_equipment', 'quant', 'manufacturer', 'model', 
      'manufacturer_serial_no', 'firmware_version', 'source_of_the_equipment', 'whether_title', 'location', 
      'room_number', 'condition', 'acquisition_date', 'original_cost', 'federal_participation',
      'comments', 'primary_tag_date', 'primary_tag_organization', 'primary_institute_asset_tag', 'secondary_tag_date',
      'second_tag_organization', 'institute_asset_tag', 'doi_tag_date', 'doi_tag_organization', 'doi_institute_asset_tag'
      ]
    data = remove_extraneous_columns(columns, newdata)
  
    id = find(db,data['ooi_barcode'])
    if id == False:
  #     data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
      res = db.insert('assets', data)
      print "Created Asset: " +data['ooi_barcode']
    else:
  #     data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
      res = db.update('assets', id, data)
      print "Updated Asset: " +data['ooi_barcode']
  else:
    print "No barcode, skipping row"


def load(db):
  """Load Assets into the database"""
  with open("repos/asset-management/bulk/bulk_load-AssetRecord.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)
