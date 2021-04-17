from downloader import Downloader
from pymongo import MongoClient
from descriptive_analysis import *
from export_collection_data import *
from datetime import datetime


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


def model_as_json(html_values):
    """ This function processes splits information from the indicator and models it on dictionaries.
        @param
            html_values:    (str or None)   a string that contains scraped information
        @return
            ip_dict:        (list)          a list of dictionaries. Each contains an IP field
    """
    ip_dict = []
    header = ["IP"]

    # each row is an IP address.
    for ip_address in html_values.split('\n'):
        # new list row each row. Lives in this for scope (what a sort life)
        my_list = list([])
        # append values
        my_list.append(ip_address)
        # zip header and current row in a dictionary
        # then append it to the list
        ip_dict.append(dict(zip(header, my_list)))

    return ip_dict

# --------------------------------------------------------------------------------------------------------------------


def add_data(dict_list):
    """ Receives a list of dictionaries and add time of crawling related data. Then returns them back
        @param
            dict_list:  (list)  a list of dictionaries. Each contains an IP field
        @return
            dict_list:  (list)  a list of enriched data dictionaries
    """
    for dict_entry in dict_list:

        datetime_utc_cti_string = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        datetime_utc_cti = datetime.strptime(datetime_utc_cti_string, '%Y-%m-%d %H:%M:%S')
        timestamp_utc_cti = datetime_utc_cti.timestamp()

        dict_entry["Category"] = "WebBasedAttacks"
        dict_entry["Entity-Type"] = "IP"
        dict_entry["TimestampUTC-CTI"] = timestamp_utc_cti
        dict_entry["mongoDate-CTI"] = datetime_utc_cti
        dict_entry["DatetimeUTC-CTI"] = datetime_utc_cti_string

    return dict_list

# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":

    crawling_time = datetime.utcnow()
    print("Report on", crawling_time.strftime('%Y-%m-%d %H:%M:%S'), '\n')

    ''' Scrape indicator '''
    # Website's URL
    URL = 'http://lists.blocklist.de/lists/all.txt'
    # prepare Downloader object
    downloader = Downloader(delay=1, cache={})
    # download a page
    html = downloader(URL)

    if html is None:
        print('Scraping Error: No content was returned\nExiting Program')
        exit(0)

    # zip IPs as dictionaries
    html_dict = model_as_json(html)
    # add time of scraping-listing
    json_data = add_data(html_dict)
    print('Scraping finished')
    # -----------------------------------------------------------------------------------------------------------------#

    ''' Store instance of scraped data in MongoDB '''
    print("\nConnecting to MongoDB Data Base")
    db = connect_to_mongodb()

    print("Storing Data...", end=' ')
    start, end = today_datetime(crawling_time)
    # delete today's data
    db.threats.webBasedAttacks1.delete_many({"mongoDate-CTI": {"$gte": start, "$lt": end}})
    # store most recent today's data
    res = db.threats.webBasedAttacks1.insert_many(json_data)
    print("Completed")
    print("Documents Inserted: ", len(res.inserted_ids))
    # -----------------------------------------------------------------------------------------------------------------#

    """ Descriptive Analysis """
    # set path of produced files
    path = '/var/www/html/saint/indicators2018/web-based-attacks/'

    # Time Series Section
    from pathlib import Path
    time_series_file = Path(path + 'perdayTimeSeriesWebBasedAttacks.json')

    # set the appropriate query
    if time_series_file.exists():
        # retrieve ONLY today's data
        today_start, today_end = today_datetime(crawling_time)
        query = {"mongoDate-CTI": {"$gte": today_start, "$lte": today_end}}
        print('\nFile perdayTimeSeriesWebBasedAttacks.json exists. Retrieve today attacks')
    else:
        # there is no analysis file, so retrieve the entire collection and create one
        query = {}
        print('\nFile perdayTimeSeriesWebBasedAttacks.json does not exist. Retrieve the entire collection')
    # set the projection
    projection = {"_id": 0, "mongoDate-CTI": 1}

    try:
        results_cursor = db.threats.webBasedAttacks1.find(query, projection)
        attack_data_frames = time_series_analysis(results_cursor, mongo_date_type='mongoDate-CTI')
        # updates both csv and json files. Specify name with NO EXTENSION
        update_time_series_analysis_files(attack_data_frames, "perdayTimeSeriesWebBasedAttacks", path)
    except Exception as e:
        print("__main__ > Descriptive Analysis Phase > Time Series Section: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None
    # -----------------------------------------------------------------------------------------------------------------#

    """ Export Datasets """
    # last datetime moment of this month must be based on crawling time to ensure synchronization
    start_of_month, end_of_month = datetime_limits_of_month(utcnow=crawling_time)

    # If you want to produce a dataset of a past month just uncomment below and modify the example
    # and change dataset name too!
    # start_of_month, end_of_month = datetime_limits_of_month(utcnow=None, set_year=2018, set_month=8)

    export_path = path + 'dataset-webBasedAttacks/'
    webBasedAttacks1_csv_header = ["IP", "Category", "Entity-Type", "TimestampUTC-CTI", "DatetimeUTC-CTI"]
    dataset_name = 'webBasedAttacks_{0}_{1}.csv'.format(crawling_time.year, crawling_time.month)

    print("\nRetrieving MongoDB's Collection...")
    try:
        query = {"mongoDate-CTI": {"$gte": start_of_month, "$lte": end_of_month}}
        projection = {"_id": 0, "mongoDate-CTI": 0}
        results_cursor = db.threats.webBasedAttacks1.find(query, projection)
        export_to_csv(results_cursor, dataset_name, webBasedAttacks1_csv_header, export_path)
    except Exception as e:
        print("__main__ > Export Datasets Phase: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    zip_directory(export_path, "dataset-webBasedAttacks.zip", path)
