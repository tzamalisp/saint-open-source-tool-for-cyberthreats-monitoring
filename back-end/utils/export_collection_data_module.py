"""
    export collection data module - Utility module to work with MongoDB's result cursors and save data to csv files
                                    Also contains auxiliary functions that define time windows based on given datetime

    Members:

        # export_to_csv             - manipulates a cursor to create a csv file with those data
        # export_to_json            - manipulates a cursor to create a json file with those data
        # zip_directory             - zips a specified directory and saves it
        # today_datetime            - calculates the first and last valid datetime objects for the day
                                      provided
        # datetime_limits_of_month  - calculates the first and last valid datetime objects for the month determined
                                      by the given datetime

"""

from datetime import datetime
import calendar
import pandas as pd
import os
from os.path import basename
import zipfile


def export_to_csv(cursor, dataset_name, csv_header, path):
    """ This function extracts data from the cursor, then produces a valid csv file with csv_header and saves it
        to the path.
    @parameters
        cursor          (cursor)    MongoDB's result cursor
        dataset_name    (str)       the name of the produced file
        csv_header      (list)      list of string that correspond to key names for each row
        path            (str)       the path to save the produced file
    """

    print("\tExporting Collection to csv File...")
    if cursor.count() == 0:
        try:
            raise Warning("No documents retrieved")
        except Exception as e:
            print("\nexport_collection_data module > export_to_csv: ", e)
            return

    doc_cursor_list = list(cursor)
    docs = pd.DataFrame(doc_cursor_list)
    docs.to_csv(path_or_buf=path+dataset_name, header=csv_header, columns=csv_header, index=False)

    # -----------------------------------------------------------------------------------------------------------------#

def export_to_json(cursor, dataset_name, path):
    """ This function extracts data from the cursor, then produces a valid json file with csv_header and saves it
        to the path.
    @parameters
        cursor          (cursor)    MongoDB's result cursor
        dataset_name    (str)       the name of the produced file
    """
    cursor = cursor.rewind()
    print("\tExporting Collection to json File...")
    if cursor.count() == 0:
        try:
            raise Warning("No documents retrieved")
        except Exception as e:
            print("\nexport_collection_data module > export_to_csv: ", e)
            return

    doc_cursor_list = list(cursor)
    docs = pd.DataFrame(doc_cursor_list)
    docs.to_json(path_or_buf=path+dataset_name, orient="records", lines=True)

    # -----------------------------------------------------------------------------------------------------------------#

def zip_directory(dir_path, zip_filename, path):
    """ This function zips a directory and saves it to the path under the name zip_filename
    @parameters
        dir_path        (str)   the file to zip
        zip_filename    (str)   the name of the zipe file
        path            (str)   the path to save the zip file
    """
    print("\tZipping Files")
    with zipfile.ZipFile(path+zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                zip_file.write(os.path.join(root, file), basename(os.path.join(root, file)))

    # -----------------------------------------------------------------------------------------------------------------#


def today_datetime(utc_now):
    """ This function returns the datetime limits for a given UTC datetime
        @parameters
            utc_now         (datetime)  the datetime to be based on
        @returns
            today_start:    (datetime)  the first moment of current day
            today_end:      (datetime)  the last moment of current day
    """

    today_start = datetime(utc_now.year, utc_now.month, utc_now.day, 0, 0, 0)
    today_end = datetime(utc_now.year, utc_now.month, utc_now.day, 23, 59, 59)

    return today_start, today_end

    # -----------------------------------------------------------------------------------------------------------------#


def datetime_limits_of_month(utcnow=None, set_year=None, set_month=None):
    """ This function returns the limits, first and last datetime, of the current month based on the current utc
        datetime or a user's selection (year, month)
        @parameters
            utcnow                  (datetime or None)  the datetime be based on. If None then the user must specify the
                                                        next two parameters
            set_year                (int or None)       any year
            set_month               (int or None)       an integer [1-12] that specifies the desired month
        @returns
            first_datetime_of_month (datetime)          the first valid moment of current or specified month in the year
            last_datetime_of_month  (datetime)          the last valid moment of current or specified month in the year
    """

    # user sets the desired month
    if set_year is not None and set_month in range(1, 13):

        number_of_days_in_month = calendar.monthrange(year=set_year, month=set_month)[1]

        first_datetime_of_month = datetime(set_year, set_month, 1, 0, 0, 0)
        last_datetime_of_month = datetime(set_year, set_month, number_of_days_in_month, 23, 59, 59)
        return first_datetime_of_month, last_datetime_of_month

    # function determines the limits based on the utcnow object
    elif utcnow is not None:

        number_of_days_in_month = calendar.monthrange(year=utcnow.year, month=utcnow.month)[1]

        first_datetime_of_month = datetime(utcnow.year, utcnow.month, 1, 0, 0, 0)
        last_datetime_of_month = datetime(utcnow.year, utcnow.month, number_of_days_in_month, 23, 59, 59)
        return first_datetime_of_month, last_datetime_of_month

    # -----------------------------------------------------------------------------------------------------------------#
