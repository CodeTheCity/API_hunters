import sys
import argparse
import datetime
import requests
import os
from requests.exceptions import HTTPError

def validate_date(start_date_text, end_date_text):
    try:
        datetime.datetime.strptime(start_date_text, '%Y-%m-%d')
        datetime.datetime.strptime(end_date_text, '%Y-%m-%d')
    except ValueError:
        print ("Incorrect data format, should be YYYY-MM-DD")

def get_csv_files(start_date_str, end_date_str, id_str):
    # Generate list of dates.
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    date_list = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days)]
    date_list.append(end_date)


    # Run a check of which sensor the id is connected to (sds011, bme280, etc).
    correct_file_format_index   = -1;
    file_format                 = ["bme280", "bpm180", "bpm280", "dht22", "ds18b20", "hpm", "htu21d", "pms5003", "pms3003", "pms7003", "ppd42ns", "sds011"]

    for iter in range(0, len(file_format)):
        file_name = "{}/{}_{}_sensor_{}.csv".format(date_list[len(date_list)-1].strftime("%Y-%m-%d"), date_list[len(date_list)-1].strftime("%Y-%m-%d"), file_format[iter], id_str)
        file_add = "http://archive.luftdaten.info/{}".format(file_name)

        try:
            request = requests.get(file_add)
            request.raise_for_status()
        except HTTPError:
           # print ("ERROR: Wrong file format \".{}\".".format(file_format[iter]))
           pass
        else:
            correct_file_format_index = iter;
            print ("SUCCESS: Found file format \".{}\".".format(file_format[iter]))

    if correct_file_format_index is -1:
        print ("ERROR: Sensor with id \'{}\' not found.".format(id_str))
    else:
        # Creating the directory data will be stored in.
        download_dir = "data/luftdaten/" + id_str
        try:
            os.makedirs(download_dir)
        except FileExistsError:
            # directory already exists
            pass

        # Download the files.
        for iter in range(0, len(date_list)):
            file_name = "{}/{}_{}_sensor_{}.csv".format(date_list[iter].strftime("%Y-%m-%d"), date_list[iter].strftime("%Y-%m-%d"), file_format[correct_file_format_index], id_str)
            file_add = "http://archive.luftdaten.info/{}".format(file_name)
            request = requests.get(file_add, stream=True)
            with open("{}/{}".format(download_dir, file_name[11:]), 'wb') as file:
                for chunk in request.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        file.write(chunk)
                print ("SUCESS: File \'{}\' successfuly downloaded.".format(file_name[11:]))

def main():
    validate_date(args["start_date"], args["end_date"])
    get_csv_files(args["start_date"], args["end_date"], args["identification"])
    

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-sd", "--start_date", required=True, help="start point from which data will downloaded")
    ap.add_argument("-ed", "--end_date", required=True, help="end point up to which data will downloaded")
    ap.add_argument("-id", "--identification", required=True, help="the ID number of the sensor that data will be downloaded for")
    args = vars(ap.parse_args())
    main()
