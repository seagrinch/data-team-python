#!/usr/bin/env python
import datateam
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal Importer')
parser.add_argument('-o','--option',
  choices=['sites', 'platforms','nodes','instruments','instrument_classes','instrument_models',
    'assets','deployments'],
  help='Type of data to load')
args = parser.parse_args()


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config()
  if args.option =="sites":
    datateam.site.load(db)
  elif args.option=="platforms":
    datateam.platform.load(db)
  elif args.option=="nodes":
    datateam.node.load(db)
  elif args.option=="instruments":
    datateam.instrument.load(db)
  elif args.option=="instrument_classes":
    datateam.instrument_class.load(db)
  elif args.option=="instrument_models":
    datateam.instrument_model.load(db)
  elif args.option=="assets":
    datateam.assets.load(db)
  elif args.option=="deployments":
    datateam.deployments.load(db)


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
