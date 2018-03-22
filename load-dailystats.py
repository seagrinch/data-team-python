#!/usr/bin/env python
# OOI Datateam Import - Load Daily Stats Data

import datateam
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal - Daily Stats Data Importer')
parser.add_argument('-s','--server',
  choices=['production','development'],
  default='development',
  help='Database server')
args = parser.parse_args()


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config(args.server)
  db.open_connection()

  # Stream Stats
  r = db.truncate_table('stream_stats')
  print "Truncated table stream_stats"

  arys = ['CE','CP','GA','GI','GP','GS','RS']
  
  # Loop over each file and import
  for ff in arys:
    dfile = 'daily_stats/%s_stream_final.csv' % (ff)
    sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE stream_stats FIELDS TERMINATED BY ',' IGNORE 1 LINES (reference_designator, method, stream, date, status);" % dfile
    a = db.sqlquery(sql);
    print "%s rows inserted from %s " % ( a.rowcount, dfile )

  # Instrument Stats
  r = db.truncate_table('instrument_stats')
  print "Truncated table instrument_stats"

  # Loop over each file and import
  for ff in arys:
    dfile = 'daily_stats/%s_refdes_final.csv' % (ff)
    sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE instrument_stats FIELDS TERMINATED BY ',' IGNORE 1 LINES (reference_designator, date, status);" % dfile
    a = db.sqlquery(sql);
    print "%s rows inserted from %s " % ( a.rowcount, dfile )

  # Finish session
  datateam.import_log.log(db,'stream_stats')
  datateam.import_log.log(db,'instrument_stats')
  db.close_connection()


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
