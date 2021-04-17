from downloader import Downloader
from pymongo import MongoClient
from descriptive_analysis import DescriptiveAnalysis
from export_collection_data import ExportCollectionData
from today_limits import today_datetime
from datetime import datetime


def connect_to_mongodb():
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

    print("Report on", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '\n')

    ''' Scrape indicator '''
    # Website's URL
    URL = 'http://lists.blocklist.de/lists/all.txt'
    # prepare Downloader object
    downloader = Downloader(delay=1, cache={})
    # download a page
    html = downloader(URL)
    # zip IPs as dictionaries
    html_dict = model_as_json(html)
    # add time of scraping-listing
    json_data = add_data(html_dict)

    ''' Connect to mongoDB '''


    ''' Store instance of scraped data in MongoDB '''
    start, end = today_datetime()
    db = connect_to_mongodb()
    # delete today's data
    db.threats.webBasedAttacks1.delete_many({"mongoDate-CTI": {"$gte": start, "$lt": end}})
    # store most recent today's data
    res = db.threats.webBasedAttacks1.insert_many(json_data)
    print("Documents Inserted: ", len(res.inserted_ids))

    """ Set Path Of Data Exportation """
    # to run on server
    server_path = '/var/www/html/saint/indicators2018/web-based-attacks/'
    # to run locally
    local_path = ""

    """ Descriptive Analysis and Result Exportation"""
    analysis = DescriptiveAnalysis(collection=db.threats.webBasedAttacks1, path=server_path)
    analysis(query={}, projection={'_id': 0})
    # returns a pandas data frame
    data_frame = analysis.time_series_analysis('mongoDate-CTI')
    # store analysis results
    analysis.data_frame_to_csv(data_frame, "perdayTimeSeriesWebBasedAttacks")
    analysis.data_frame_to_json(data_frame, "perdayTimeSeriesWebBasedAttacks")
    # top10 = analysis.top_n(10,"IP", "web-based-attacks-top-IPs")
    # print(top10)

    ''' Export current MongoDB collection instance '''
    # webBasedAttacks_collection = ExportCollectionData(collection=db.threats.webBasedAttacks1, path=server_path)
    # webBasedAttacks_collection(query={}, projection={"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0})
    # webBasedAttacks_collection.export_collection_to_json("dataset-webBasedAttacks")
    #
    # csv_header = ["IP", "Category", "Entity-Type", "TimestampUTC-CTI", "DatetimeUTC-CTI"]
    # webBasedAttacks_collection.export_collection_to_csv("dataset-webBasedAttacks", csv_header)


