from pymongo import MongoClient
from datetime import datetime, timedelta
from downloader import Downloader
from descriptive_analysis import *
from export_collection_data import *

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


def get_content(html_code):
    """ Separates the webpage's message section from the content section and returns both for further processing
        @parameters
            html_code   (str)       html code of the downloaded web page
        @returns
            tuple       (of lists)  message_list: list of strings. Each string is a line from MESSAGE section (webpage)
                                    content_list: list of strings. Each string is a line from CONTENT section (webpage)
    """

    message_list, content_list = [], []

    for line in html_code.split('\n'):
        if line.startswith('#') and not line.endswith('#'):
            message_list.append(line)
        elif not line.endswith('#'):
            content_list.append(line)
    return message_list, content_list

# -------------------------------------------------------------------------------------------------------------------- #


def aggregate_content(html_content):
    """ This function models html content into a dictionary form
        @param
            html_content    (list)  each item of this list is a string representation of a line from c2-ipmasterlist.txt
        @returns
            dict_list       (list)  this list contains the dictionary representation of each html_content line
    """

    data_list = []

    for line in html_content:

        if line == "":
            # "" is present at the end of ipmasterlsit.txt
            continue

        items = [word for word in line.split(',')]  # split line and turn it into a list of word

        ''' IP objects '''
        # ip
        ip = items[0]

        # ip user
        ip_user = ""
        for word in items[1].split():
            if word not in ["IP", "used", "by"]:
                ip_user += word + " "

        ''' Time objects '''
        # utc datetime of event
        datetime_utc = datetime.strptime(items[2], '%Y-%m-%d %H:%M')
        # string representation
        datetime_utc_string = str(datetime_utc)
        # utc timestamp of event
        timestamp_utc = float(datetime_utc.timestamp())

        datetime_utc_cti_string = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        datetime_utc_cti = datetime.strptime(datetime_utc_cti_string, '%Y-%m-%d %H:%M:%S')
        timestamp_utc_cti = float(datetime_utc_cti.timestamp())

        ''' Description Object '''
        description = items[3]

        row_list = ["Botnets", "IP", ip, ip_user, timestamp_utc, datetime_utc, datetime_utc_string,
                    timestamp_utc_cti, datetime_utc_cti, datetime_utc_cti_string, description]
        data_list.append(row_list)

    return data_list

# -------------------------------------------------------------------------------------------------------------------- #


def model_as_json(data_array):

    # row_list = ["Botnets", "IP", ip, ip_user, utc_timestamp, utc_datetime,
    #   cti_utc_timestamp, cti_utc_datetime, description]
    json_list = []

    for entry in data_array:

        json_object = {
            "_id": {"IP": entry[2], "TimestampUTC": entry[4], "IP User": entry[3]},
            "Category": entry[0],
            "Entity-Type": entry[1],
            "IP": entry[2],
            "IP-User": entry[3],
            "TimestampUTC": entry[4],
            "mongoDate": entry[5],
            "DatetimeUTC": entry[6],
            "TimestampUTC-CTI": entry[7],
            "mongoDate-CTI": entry[8],
            "DatetimeUTC-CTI": entry[9],
            "Description": entry[10],
        }

        json_list.append(json_object)

    return json_list

# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':

    crawling_time = datetime.utcnow()
    print("Report on", crawling_time.strftime('%Y-%m-%d %H:%M:%S'), '\n')

    ''' Scrape Indicator '''
    # indicator URL
    URL = 'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt'

    downloader = Downloader(delay=1, cache={})      # prepare Downloader object
    html = downloader(URL)                          # download a page

    if html is None:
        print('Scraping Error: No content was returned\nExiting Program')
        exit(0)

    message, page_content = get_content(html)
    data = aggregate_content(page_content)
    json_processed_data = model_as_json(data)
    print("Scraping Finished")
    # -----------------------------------------------------------------------------------------------------------------#

    ''' Store instance of scraped data in MongoDB '''
    print("\nConnecting to MongoDB Data Base")
    db = connect_to_mongodb()
    docs_match_update, docs_modified_update, docs_inserted = 0, 0, 0

    print("Storing Data...", end=' ')
    for doc in json_processed_data:
        upd_res = db.threats.ipmasterlist.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
        docs_match_update += upd_res.matched_count
        docs_modified_update += upd_res.modified_count
        if upd_res.upserted_id is not None:
            docs_inserted += 1

    print("Completed")
    print("\tDocuments Inserted: ", docs_inserted)
    print("\tDocuments Matched Update Filter: ", docs_match_update)
    print("\tDocuments Modified: ", docs_modified_update)
    # -----------------------------------------------------------------------------------------------------------------#

    """ Descriptive Analysis """
    # set path of produced files
    path = '/var/www/html/saint/indicators2018/botnets/'

    # Time Series Section
    from pathlib import Path
    time_series_file = Path(path + 'perdayTimeSeriesBotnets.json')

    # set the appropriate query
    if time_series_file.exists():
        # retrieve ONLY today's data
        today_start, today_end = today_datetime(crawling_time)
        query = {"mongoDate": {"$gte": today_start, "$lte": today_end}}
        print('\nFile perdayTimeSeriesBotnets.json exists. Retrieve today attacks')
    else:
        # there is no analysis file, so retrieve the entire collection and create one
        query = {}
        print('\nFile perdayTimeSeriesBotnets.json does not exist. Retrieve the entire collection')
    # set the projection
    projection = {"_id": 0, "mongoDate": 1}

    try:
        results_cursor = db.threats.ipmasterlist.find(query, projection)
        attack_data_frames = time_series_analysis(results_cursor, mongo_date_type='mongoDate')
        # updates both csv and json files. Specify name with NO EXTENSION
        update_time_series_analysis_files(attack_data_frames, "perdayTimeSeriesBotnets", path)
    except Exception as e:
        print("__main__ > Descriptive Analysis Phase > Time Series Section: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    # Barplot Section
    last_week = datetime.utcnow() - timedelta(days=7)
    query = {"mongoDate": {"$gte": last_week}}
    projection = {"_id": 0}

    try:
        last_week_results_cursor = db.threats.ipmasterlist.find(query, projection)
        # find last weeks top 10 countries and save them to csv and json. Specify name with NO EXTENSION
        top_countries = top_n(last_week_results_cursor, 10, 'IP', 'botnets-top-ips', path)
        print("\nLast Week's Top Botnet IPs\n", top_countries)
    except Exception as e:
        print("__main__ > descriptive analysis phase > Barplot Analysis: ", e)
        # destroy cursor, it won't be used again
        last_week_results_cursor = None
    # -----------------------------------------------------------------------------------------------------------------#

    """ Export Datasets """
    # last datetime moment of this month must be based on crawling time to ensure synchronization
    start_of_month, end_of_month = datetime_limits_of_month(utcnow=crawling_time)

    # If you want to produce a dataset of a past month just uncomment below and modify the example
    # and change dataset name too!
    # start_of_month, end_of_month = datetime_limits_of_month(utcnow=None, set_year=2018, set_month=8)

    export_path = path + 'dataset-botnets/'
    ipmasterlist_csv_header = ["Category", "Entity-Type", "IP", "IP-User", "TimestampUTC", "DatetimeUTC",
                               "TimestampUTC-CTI", "DatetimeUTC-CTI", "Description"]
    dataset_name = 'botnets_{0}_{1}.csv'.format(crawling_time.year, crawling_time.month)

    print("\nRetrieving MongoDB's Collection...")
    try:
        query = {"mongoDate": {"$gte": start_of_month, "$lte": end_of_month}}
        projection = {"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0}
        results_cursor = db.threats.ipmasterlist.find(query, projection)
        export_to_csv(results_cursor, dataset_name, ipmasterlist_csv_header, export_path)
    except Exception as e:
        print("__main__ > Export Datasets Phase: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    zip_directory(export_path, "dataset-botnets.zip", path)