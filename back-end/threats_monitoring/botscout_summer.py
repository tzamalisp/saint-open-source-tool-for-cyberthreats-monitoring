from pymongo import MongoClient
from datetime import datetime, timedelta
from lxml.html import fromstring
from downloader import Downloader
from descriptive_analysis import DescriptiveAnalysis
from export_collection_data import ExportCollectionData


def connect_to_mongodb():
    """ This function implements the connection to the mongoDb
        :returns
            connection  (MongoClient)   a MongoClient object to handle the connection
    """

    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    return db

# -------------------------------------------------------------------------------------------------------------------- #


def scrape_it(html):
    """ Scrapes all the need data from the downloaded web page
        :parameter
            html    (str)   html source code (never None) of downloaded page
        :return
            values  (list)  list with all scraped values
    """

    tree = fromstring(html)

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


def validate_and_enrich_time(data_array):
    """ This function validates time goodies and returns them
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

    return datetime_obj + timedelta(hours=hour_interval)

# -------------------------------------------------------------------------------------------------------------------- #


def model_as_json(bot_entries):

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

    print("Report on", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '\n')

    ''' Scrape Indicator '''
    # indicator URL
    URL = "http://botscout.com/last.htm"

    downloader = Downloader(delay=1, cache={})      # prepare Downloader object
    html = downloader(URL)                          # download a page
    if html is None:                                # if None returned no content found, so exit
        print('Scraping Error: No content was returned')
        exit(0)
    # data is a list of lists.
    # each sub-list is a bot entry
    data = scrape_it(html)
    clean_data = validate_and_enrich_time(data)
    json_modeled_data = model_as_json(clean_data)


    ''' Store instance of scraped data in MongoDB '''
    db = connect_to_mongodb()

    docs_match_update, docs_modified_update, docs_inserted  = 0, 0, 0

    for doc in json_modeled_data:
        upd_res = db.threats.botscout.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert = True)
        #print(doc["DatetimeUTC"], type(doc["DatetimeUTC"]), upd_res.modified_count)
        docs_match_update += upd_res.matched_count
        docs_modified_update += upd_res.modified_count
        if upd_res.upserted_id is not None:
            docs_inserted += 1

    print("Documents Inserted: ", docs_inserted)
    print("Documents Matched Update Filter: ", docs_match_update)
    print("Documents Modified: ", docs_modified_update)
    print()

    """ Set Path Of Data Exportation """
    # to run on server
    server_path = '/var/www/html/saint/indicators2018/botnets/'
    # to run locally
    local_path = ""

    """ Descriptive Analysis and Result Exportation"""
    analysis = DescriptiveAnalysis(collection=db.threats.botscout, path=server_path)
    analysis(query=None, projection=None)
    # returns a pandas data frame
    data_frame = analysis.time_series_analysis('mongoDate')
    # store analysis results
    analysis.data_frame_to_csv(data_frame, "perdayTimeSeriesBotnetsDetailed")
    analysis.data_frame_to_json(data_frame, "perdayTimeSeriesBotnetsDetailed")

    last_week = datetime.utcnow() - timedelta(days=7)
    analysis_2 = DescriptiveAnalysis(collection=db.threats.botscout, path=server_path)
    analysis_2(query={'mongoDate': {"$gte": last_week}}, projection={"_id": 0})
    top_countries = analysis_2.top_n(10, "Country", 'botnets-detailed-top-countries')
    print(top_countries)

    ''' Export current MongoDB collection instance '''
    # botscout_collection = ExportCollectionData(collection=db.threats.botscout, path=server_path)
    # # apply the query to collection, absence parameters means use the default
    # # collections data will be available at query_result class variable
    # documents_retrieved = botscout_collection()
    # botscout_collection.export_collection_to_json("dataset-botnets-detailed")
    #
    # csv_header = ["Category", "Entity-Type", "IP", "Botscout-id", "Bot-Name", "Email", "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI", "Country"]
    # botscout_collection.export_collection_to_csv("dataset-botnets-detailed", csv_header)

