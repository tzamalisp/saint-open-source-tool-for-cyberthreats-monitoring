from pymongo import MongoClient
from datetime import datetime, timedelta
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


def get_content(html_code):
    """ Separates the message section from the content section and returns the for further process
        :parameters
            html_code   (str)   html code  of the downloaded
        :returns
            tuple       (lists) the tuple returned contains two lists of strings. Each list item is a line
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
        :param
            html_content    (list)  each item of this list is a string representation of a line from c2-ipmasterlist.txt
        :returns
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

    print("Scraping Finished")

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

    # csv_header = [
    #   "Category", "Entity Type", "IP", "IP User", "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI",
    #   "DatetimeUTC-CTI", "Description" "Host", "Host_IP", "RDNS", "ASN", "ISP", "Country Name", "Country Code",
    #   "Region", "City", "Postal Code", "Continent Code", "Latitude", "Longitude", "DMA Code", "Area Code", "Timezone"
    # ]

    print("Report on", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '\n')

    ''' Scrape Indicator '''
    # indicator URL
    URL = 'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt'

    downloader = Downloader(delay=1, cache={})      # prepare Downloader object
    html = downloader(URL)                          # download a page
    if html is None:                                # if None returned no content found, so exit
        print('Scraping Error: No content was returned')
        exit(0)

    message, page_content = get_content(html)
    data = aggregate_content(page_content)
    json_processed_data = model_as_json(data)


    ''' Store instance of scraped data in MongoDB '''
    db = connect_to_mongodb()

    docs_match_update, docs_modified_update, docs_inserted  = 0, 0, 0

    for doc in json_processed_data:
        upd_res = db.threats.ipmasterlist.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert = True)
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

    """ Descriptive Analysis and Result Exportation """
    analysis = DescriptiveAnalysis(collection=db.threats.ipmasterlist, path=server_path)
    analysis(query={}, projection={"_id": 0})
    # returns a pandas data frame
    data_frame = analysis.time_series_analysis('mongoDate')
    # store analysis results
    analysis.data_frame_to_csv(data_frame, "perdayTimeSeriesBotnets")
    analysis.data_frame_to_json(data_frame, "perdayTimeSeriesBotnets")

    last_week = datetime.utcnow() - timedelta(days=7)
    analysis_2 = DescriptiveAnalysis(collection=db.threats.ipmasterlist, path=server_path)
    analysis_2(query={'mongoDate': {"$gte": last_week}}, projection={"_id": 0})
    analysis_2.top_n(10, "IP", "botnets-top-ips")

    ''' Export current MongoDB collection instance '''
    # ipmasterlist_collection = ExportCollectionData(collection=db.threats.ipmasterlist, path=server_path)
    # ipmasterlist_collection(query={}, projection={"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0})
    # ipmasterlist_collection.export_collection_to_json("dataset-botnets")
    #
    # csv_header = ["Category", "Entity-Type", "IP", "IP-User", "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI", "Description"]
    # ipmasterlist_collection.export_collection_to_csv("dataset-botnets", csv_header)

