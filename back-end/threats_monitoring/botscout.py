from pymongo import MongoClient
from lxml.html import fromstring
from downloader import Downloader
from descriptive_analysis import *
from export_collection_data import *
from datetime import datetime, timedelta
import numpy as np


def connect_to_mongodb():
    """ This function implements the connection to the mongoDb
        @returns
            connection  (MongoClient)   a MongoClient object to handle the connection
    """
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    return db

# -------------------------------------------------------------------------------------------------------------------- #


def scrape_it(html_code):
    """ Scrapes all the need data from the downloaded web page
        @parameter
            html_code    (str)   html source code (never None) of downloaded page
        @return
            bot_entries  (list)  list of all scraped values
    """

    tree = fromstring(html_code)

    bot_entries = []
    content = tree.xpath('//td/text()')[6:]
    ip = tree.xpath('//td/a/text()')
    country = tree.xpath('//td/a/img/@title')

    num_rows = len(ip)

    for i in range(0, num_rows):
        position_of_entry = i*4
        row = [ip[i]] + [country[i]] + content[position_of_entry:position_of_entry+4]
        bot_entries.append(row)
        # print(i, position_of_entry, position_of_entry+1, position_of_entry+2, position_of_entry+3, row)

    return bot_entries

# -------------------------------------------------------------------------------------------------------------------- #


def validate_time(data_array):
    """ This function validates time goodies and returns them
        @parameter
            data_array  (list)  a list of sub-lists. Each sublist contains bot entries
        @returns
            data_array  (list)  a list of sub-lists. Each sublist contains VALIDATED bot entries
    """

    for row in data_array:
        date_string = row[3]

        datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %I:%M %p')
        datetime_utc = fix_hour_utc(datetime_obj, +5)
        timestamp_utc = float(datetime_utc.timestamp())
        datetime_utc_string = str(datetime_utc)

        datetime_utc_cti_string = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        datetime_utc_cti = datetime.strptime(datetime_utc_cti_string, '%Y-%m-%d %H:%M:%S')
        timestamp_utc_cti = float(datetime_utc_cti.timestamp())

        row.append(timestamp_utc)
        row.append(datetime_utc)
        row.append(datetime_utc_string)

        row.append(timestamp_utc_cti)
        row.append(datetime_utc_cti)
        row.append(datetime_utc_cti_string)

    return data_array

# -------------------------------------------------------------------------------------------------------------------- #


def fix_hour_utc(datetime_obj, hour_interval):
    """ This function adds some hours in a datetime object
    @param
        datetime_obj    (datetime)
        hour_interval   (int)       represents the hours to add
    @returns
        a new datetime time object
    """
    return datetime_obj + timedelta(hours=hour_interval)

# -------------------------------------------------------------------------------------------------------------------- #


def model_as_json(bot_entries):
    """ Casts a list of lists into a list of modeled dictionaries. New data format is JSON-like and suitable for MongoDB
        @param
            bot_entries     (list)      list of sub-lists
        @returns
            json_list       (list)      list of modeled dictionaries
    """

    json_list = []

    for bot_entry in bot_entries:
        json_object = {
            "_id": bot_entry[2],
            "Category": "Botnets",
            "Entity-Type": "IP",
            "IP": bot_entry[0],
            "Botscout-id": bot_entry[2],
            "Bot-Name": bot_entry[4],
            "Email": bot_entry[5],
            "TimestampUTC": bot_entry[6],
            "mongoDate": bot_entry[7],
            "DatetimeUTC": bot_entry[8],
            "TimestampUTC-CTI": bot_entry[9],
            "mongoDate-CTI": bot_entry[10],
            "DatetimeUTC-CTI": bot_entry[11],
            "Country": bot_entry[1],
        }

        json_list.append(json_object)

    return json_list

# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':

    crawling_time = datetime.utcnow()
    print("Report on", crawling_time.strftime('%Y-%m-%d %H:%M:%S'), '\n')

    ''' Scrape Indicator '''
    indicator_url = "http://botscout.com/last.htm"
    downloader = Downloader(delay=1, cache={})
    html = downloader(indicator_url)

    if html is None:
        print('Scraping Error: No content was returned\nExiting Program')
        exit(0)

    # data is a list of sub-lists, each sub-list is a bot entry
    data = scrape_it(html)
    clean_data = validate_time(data)
    json_modeled_data = model_as_json(clean_data)
    print('Scraping finished')
    # ---------------------------------------------------------------------------------------------------------------- #

    ''' Store scraped data in MongoDB '''
    print("\nConnecting to MongoDB Data Base")
    db = connect_to_mongodb()
    docs_match_update, docs_modified_update, docs_inserted = 0, 0, 0

    print("Storing Data...", end=' ')
    for doc in json_modeled_data:
        upd_res = db.threats.botscout.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
        # print(doc["DatetimeUTC"], type(doc["DatetimeUTC"]), upd_res.modified_count)
        docs_match_update += upd_res.matched_count
        docs_modified_update += upd_res.modified_count
        if upd_res.upserted_id is not None:
            docs_inserted += 1

    print("Completed")
    print("\tDocuments Inserted: ", docs_inserted)
    print("\tDocuments Matched Update Filter: ", docs_match_update)
    print("\tDocuments Modified: ", docs_modified_update)
    # ---------------------------------------------------------------------------------------------------------------- #

    """ Descriptive Analysis """
    # set path of produced files
    path = '/var/www/html/saint/indicators2018/botnets/'

    # Time Series Section
    from pathlib import Path
    time_series_file = Path(path + 'perdayTimeSeriesBotnetsDetailed.json')

    # set the appropriate query
    if time_series_file.exists():
        # retrieve ONLY today's data
        today_start, today_end = today_datetime(crawling_time)
        query = {"mongoDate": {"$gte": today_start, "$lte": today_end}}
        print('\nFile perdayTimeSeriesBotnetsDetailed.json exists. Retrieve today attacks')
    else:
        # there is no analysis file, so retrieve the entire collection and create one
        query = {}
        print('\nFile perdayTimeSeriesBotnetsDetailed.json does not exist. Retrieve the entire collection')
    # set the projection
    projection = {"_id": 0, "mongoDate": 1}

    try:
        results_cursor = db.threats.botscout.find(query, projection)
        attack_data_frames = time_series_analysis(results_cursor, mongo_date_type='mongoDate')
        # updates both csv and json files. Specify name with NO EXTENSION
        update_time_series_analysis_files(attack_data_frames, "perdayTimeSeriesBotnetsDetailed", path)
    except Exception as e:
        print("__main__ > Descriptive Analysis Phase > Time Series Section: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    # Barplot Section
    last_week = datetime.utcnow() - timedelta(days=7)
    query = {"mongoDate": {"$gte": last_week}}
    projection = {"_id": 0}

    try:
        last_week_results_cursor = db.threats.botscout.find(query, projection)
        # find last weeks top 10 countries and save them to csv and json. Specify name with NO EXTENSION
        top_countries = top_n(last_week_results_cursor, 10, 'Country', 'botnets-detailed-top-countries', path)
        print("\nLast Week's Top Botnet Countries\n", top_countries)
    except Exception as e:
        print("__main__ > descriptive analysis phase > Barplot Analysis: ", e)
        # destroy cursor, it won't be used again
        last_week_results_cursor = None
    # ---------------------------------------------------------------------------------------------------------------- #

    """ Export Datasets """
    # last datetime moment of this month must be based on crawling time to ensure synchronization
    start_of_month, end_of_month = datetime_limits_of_month(utcnow=crawling_time)

    # If you want to produce a dataset of a past month just uncomment below and modify the example
    # and change dataset name too!
    # start_of_month, end_of_month = datetime_limits_of_month(utcnow=None, set_year=2018, set_month=8)

    export_path = path + 'dataset-botnets-detailed/'
    botscout_csv_header = ['Category', 'Entity-Type', 'IP', 'Botscout-id', 'Bot-Name', 'Email', 'TimestampUTC',
                           'DatetimeUTC', 'TimestampUTC-CTI', 'DatetimeUTC-CTI', 'Country']
    dataset_name = 'botnets-detailed_{0}_{1}.csv'.format(crawling_time.year, crawling_time.month)

    print("\nRetrieving MongoDB's Collection...")
    try:
        query = {"mongoDate": {"$gte": start_of_month, "$lte": end_of_month}}
        projection = {"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0}
        results_cursor = db.threats.botscout.find(query, projection)
        export_to_csv(results_cursor, dataset_name, botscout_csv_header, export_path)
        
    except Exception as e:
        print("__main__ > Export Datasets Phase: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    zip_directory(export_path, "dataset-botnets-detailed.zip", path)
