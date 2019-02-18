# API_hunters
Team API Hunters at CTC15

The goal, we want to download .csv files from (luftdaten.info and madavi.de) using python. At the moment, there is no API to access uploaded data; instead CSVs have to be downloaded from the luftdaten/madavi and then re-amalgamated. The issue, it is too time consuming to individually download the required .csv files, by hand. 


# Usage

Downloading a month worth of data for a particular sensor off luftdaten so far is achieved by the command:

```luftdaten.py -sd 2019-01-15 -ed 2019-02-15 -id 15092```

Where ```-sd``` is start date and ```-ed``` is end date, ```-id``` is the luftdaten id of the sensor.

# Dependencies 

Getting the script to work requires two prerequisites, obtained through:

```pip install requests```

```pip install python-dateutil```
