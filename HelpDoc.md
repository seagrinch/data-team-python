# How to run the backend scripts
This page includes additional information on how to run each of the included scripts to update the OOI Data Team Portal database.  For more information, please see [Readme.md](Readme.md).  

Note, these scrips make use of the library files found in [datateam](datateam) directory.  Most functions in the library are fairly straightforward, loading data from CSV files from various associated GitHib repos (see the readme), and additional methods for inserting the parsed information into the database.  

The scripts below provide high-level methods to batch load all of the data at once.

## load-annotations.py
This script retrieves the latest annotations from the OOI Data Portal (aka uFrame) and adds them to the Data Team Portal database.  In order for this script to work, you will need to specify your OOINet API username and password in config.cfg, as well as your mysql database configuration.

#### Options
* **-s --server** Specifies which database connection to use from the configuration file.  Specify either "development" (the default) or "production".


## load-dailystatys.py
This script loads the daily instrument statistics information calculated by the scripts available in the [ooi-stats](https://github.com/ooi-data-review/ooi_stats) repo.

#### Options
* **-s --server** Specifies which database connection to use from the configuration file.  Specify either "development" (the default) or "production".
* **-d --directory** The directory where the stats output can be found.

### Example
`./load-dailystats.py -s production -d /home/knuth/ooi_stats/stats/output/`

    
## load-data.py
This script can be used to load and update most of the metadata needed for the OOI Data Team portal.  It uses information found in various other GitHub repositories managed by the OOI program.

#### Options
* **-s --server** Specifies which database connection to use from the configuration file.  Specify either "development" (the default) or "production".
* **-o --option** Specifies which type of data to load.  This parameter is required.  The available options follow.  This is also the suggested order which should be used when initially loading all data into the system, as some of the later items depend on earlier items already being in the database.
  * **regions** - List of Arrays from [infrastructure/regions.csv](infrastructure/regions.csv)
  * **sites** - Sites from [infrastructure/sites.csv](infrastructure/sites.csv)
  * **nodes** - Nodes from [infrastructure/nodes.csv](infrastructure/nodes.csv)
  * **instruments** - Instruments (reference designators) from [infrastructure/instruments.csv](infrastructure/instruments.csv)
  * **instrument_classes** - Instrument Classes from [infrastructure/instrument_classes.csv](infrastructure/instrument_classes.csv)
  * **instrument_models** - Instrument Models from [infrastructure/instrument_models.csv](infrastructure/instrument_models.csv)
  * **assets** - Assets (individual sensors) from [ooi-integration asset-management/bulk](https://github.com/ooi-integration/asset-management/tree/master/bulk)
  * **cruises** - Cruises from [ooi-integration asset-management/cruise](https://github.com/ooi-integration/asset-management/tree/master/cruise)
  * **deployments** - Deployment information from [ooi-integration asset-management/deployment](https://github.com/ooi-integration/asset-management/tree/master/deployment)
  * **calibrations** - Calibration values from [ooi-integration asset-management/calibration](https://github.com/ooi-integration/asset-management/tree/master/calibration)
  * **preload** - Loads parameters, parameter_functions, streams, and parameter/stream links from [oceanobservatories preload-database](https://github.com/oceanobservatories/preload-database.git).  In addition, the description for some streams is overridden with the descriptions found in [infrastructure/stream_descriptions.csv](infrastructure/stream_descriptions.csv).  Note, before this option can be run, the preload sqlite database must be updated.  You can use the [preload_update_db.sh](preload_update_db.sh) script to do this. 
  * **data_streams** - Data Streams from [infrastructure/data_streams.csv](infrastructure/data_streams.csv)
  * **ingestions** - Ingestions from [ooi-integration ingestion-csvs](https://github.com/ooi-integration/ingestion-csvs.git)

### Example
`./load-data.py -s production -o regions`


## load-status.py
This script will ping the OOI Data Portal (via the API) to request the last 48 hours of data for each instrument.  If data is returned, it will update the current_status column in the Data Team Portal.  

Note that this script only checks instruments that do not already have a current_status defined in [infrastructure/instruments.csv](infrastructure/instruments.csv).  This allows non-real-time instruments (e.g. lost, suspended, etc.) to be excluded from the status check.  It can also be used to exclude non-essential instruments (e.g. engineering ones).  

The preferred_stream and preferred_parameter columns in the instruments file are used to specify which stream/parameter should be checked to verify whether an instrument is operation in real-time.  The method (telemetered or streamed) is automatically determined by the script.

In order for this script to work, you will need to specify your OOINet API username and password in config.cfg, as well as your mysql database configuration.

This script will also output a dated CSV file containing the status of all instruments checked.

#### Options
* **-s --server** Specifies which database connection to use from the configuration file.  Specify either "development" (the default) or "production".
