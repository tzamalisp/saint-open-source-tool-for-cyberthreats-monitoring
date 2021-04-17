from pymongo import MongoClient
from datetime import datetime
from bs4 import BeautifulSoup
import re
from downloader import Downloader
from export_collection_data import ExportCollectionData
from descriptive_analysis import DescriptiveAnalysis


def connect_to_mongodb():
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    return db

    # ---------------------------------------------------------------------------------------------------------------- #


def crawl_ransomware_lists(html_code):
    """ Scrapes all the need data from the downloaded web page
        @parameter
            html    (str)   html source code (never None) of downloaded page
        @retukrn
            values  (list)  list with all scraped values
    """

    soup = BeautifulSoup(html_code, 'lxml')

    second_table_rows = soup.find_all('table')[1]
    td_elements = second_table_rows.find_all('td')
    block_lists = list([])

    for i in range(0, len(td_elements), 6):

        try:
            relative_link = td_elements[i+5].a.get('href')
            absolute_link = 'https://ransomwaretracker.abuse.ch' + relative_link
        except Exception:
            print("No link assigned for this list. Skip it")
            continue

        row_dict = {
            # row_list.append(td_elements[i].string)
            "Malware-Type": td_elements[i + 1].string,
            "Scope": td_elements[i + 2].string,
            "Blocklist-Type": [word for word in td_elements[i + 3].string.split(' ') if word in ['URL', 'Domain', 'IP']][0],
            "FP-Risk": td_elements[i + 4].string,
            "link": absolute_link
        }
        block_lists.append(row_dict)

    return block_lists

    # ---------------------------------------------------------------------------------------------------------------- #


def scrape_content(blocklist_dicts, downloader):

    for block_dict in blocklist_dicts:

        data = downloader(block_dict['link'])
        block_dict['html_content'] = data

    return blocklist_dicts

    # ---------------------------------------------------------------------------------------------------------------- #


def clean_and_model_data(blocklist_dicts):

    exp = re.compile('([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])) [0-9]{2}:[0-9]{2}:[0-9]{2}')

    # prepare cti datetime
    datetime_utc_cti_string = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    datetime_utc_cti = datetime.strptime(datetime_utc_cti_string, '%Y-%m-%d %H:%M:%S')
    timestamp_utc_cti = float(datetime_utc_cti.timestamp())

    # if no data about generation date is found
    # or an re error occurs then generation time will be set to cti crawling-discovering time
    datetime_utc_string = datetime_utc_cti_string
    datetime_utc = datetime_utc_cti_string
    timestamp_utc = timestamp_utc_cti

    for dict in blocklist_dicts:

        modeled_data = list([])
        # if the data generation date is not found in the text file we will set cti crawling time a generation time
        if dict['html_content'] is not None:

            # process html content
            html = dict['html_content']
            # a dictionary to model data
            lines = html.split('\n')

            for line in lines:

                if "Generated on" in line:
                    try:
                        datetime_utc_string = exp.search(line).group()
                        datetime_utc = datetime.strptime(datetime_utc_string, "%Y-%m-%d %H:%M:%S")
                        timestamp_utc = datetime_utc.timestamp()
                    except TypeError as e:
                        print("Type error of 'Generated on Time': ", e)
                        datetime_utc_string = datetime_utc_cti_string
                        datetime_utc = datetime_utc_cti_string
                        timestamp_utc = timestamp_utc_cti

                elif line.startswith('#'):  # and regular expression:
                    continue
                else:
                    line.strip(' ')
                    # if line is empty
                    if line == '':
                        continue

                    entry = {
                        "Category": "Ransomware",
                        "Subcategory": dict["Malware-Type"],
                        "Entity-Type": dict["Blocklist-Type"],
                        "Scope": dict["Scope"],
                        dict["Blocklist-Type"]: line,
                        "False-Positive-Risk": dict["FP-Risk"],
                        "TimestampUTC": timestamp_utc,
                        "mongoDate": datetime_utc,
                        "DatetimeUTC": datetime_utc_string,
                        "TimestampUTC-CTI": timestamp_utc_cti,
                        "mongoDate-CTI": datetime_utc_cti,
                        "DatetimeUTC-CTI": datetime_utc_cti_string
                    }
                    modeled_data.append(entry)

        dict["data"] = modeled_data

    return blocklist_dicts

    # ---------------------------------------------------------------------------------------------------------------- #


def aggregate_lists(blocklist_dicts):

    top_list = list([])

    for dictionary in blocklist_dicts:
        for entry in dictionary["data"]:
            top_list.append(entry)

    return top_list

    # ---------------------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':

    print("Report on", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '\n')

    ''' Scrape Indicator '''
    # indicator URL
    URL = "https://ransomwaretracker.abuse.ch/blocklist/"

    downloader = Downloader(delay=1)      # prepare Downloader object
    html = downloader(URL)                # download a page
    if html is None:                      # if None returned no content found, so exit
        print('Scraping Error: No content was returned')
        exit(0)
    # data is a list of dictionaries.
    blocklists = crawl_ransomware_lists(html)
    # list of dictionaries. Html content of web page was added to each dictionary
    downloaded_blocklists = scrape_content(blocklists, downloader)
    # separate data from comments
    structrured_data = clean_and_model_data(downloaded_blocklists)
    # returns a list of aggregated dictionaries of all type (IP, URL, Domain)
    total_list_data = aggregate_lists(structrured_data)

    ''' Store instance of scraped data in MongoDB '''
    db = connect_to_mongodb()

    # start, end = today_datetime()
    # # delete today's data
    # print(start, end)
    # res_d = db.threats.ransomware.delete_many({"mongoDate-CTI": {"$gte": start, "$lt": end}})
    # print("Documents Deleted: ", res_d.deleted_count)
    db.threats.ransomware.drop()
    # import recent instance
    res = db.threats.ransomware.insert_many(total_list_data)
    print("Documents Inserted: ", len(res.inserted_ids))

    """ Set Path Of Data Exportation """
    # to run on server
    server_path = '/var/www/html/saint/indicators2018/ransomware/'
    # to run locally
    local_path = ""

    """ Descriptive Analysis and Result Exportation"""
    analysis = DescriptiveAnalysis(collection=db.threats.ransomware, path=server_path)
    # call object to query collection. No arguments chooses default parameters {}
    # returns num of doc results
    analysis(query={}, projection={"_id": 0})
    # returns a pandas data frame
    # ransomware_data_frame = analysis.time_series_analysis('mongoDate-CTI')
    # store analysis results
    # analysis.data_frame_to_csv(ransomware_data_frame, "perdayTimeSeriesRansomware")
    # analysis.data_frame_to_json(ransomware_data_frame, "perdayTimeSeriesRansomware")
    top3_entity_types = analysis.top_n(3, "Entity-Type", 'ransomware-top-entity-types')
    top5_scope = analysis.top_n(5, "Scope", 'ransomware-top-scope')
    top5_subcategories = analysis.top_n(5, "Subcategory", "ransomware-top-subcategories")
    print("Top Entity Type: ", top3_entity_types)
    print("Top Scope: ", top5_scope)
    print("Top Subcategories: ", top5_subcategories)

    ''' Export current MongoDB collection instance '''
    ransomware_collection = ExportCollectionData(collection=db.threats.ransomware, path=server_path)
    # apply the query to collection, absence parameters means use the default
    # collections data will be available at query_result class variable
    documents_retrieved = ransomware_collection()

    """ Export to JSON """
    # ransomware_collection.export_collection_to_json("dataset-ransomware-IP", "IP")
    # ransomware_collection.export_collection_to_json("dataset-ransomware-URL", "URL")
    # ransomware_collection.export_collection_to_json("dataset-ransomware-Domain", "Domain")
    # ransomware_collection.export_collection_to_json("dataset-ransomware-all")
    #
    # """ Export collection to CSV """
    # # prepare csv headers
    # csv_header = {
    #     "IP": ["Category", "Subcategory", "Entity-Type", "Scope", "IP", "False-Positive-Risk",
    #         "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI"],
    #
    #     "URL": ["Category", "Subcategory", "Entity-Type", "Scope", "URL", "False-Positive-Risk",
    #         "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI"],
    #
    #     "Domain": ["Category", "Subcategory", "Entity-Type", "Scope", "Domain", "False-Positive-Risk",
    #         "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI"]
    # }
    # ransomware_collection.export_collection_to_csv("dataset-ransomware-IP", csv_header["IP"], "IP")
    # ransomware_collection.export_collection_to_csv("dataset-ransomware-URL", csv_header["URL"], "URL")
    # ransomware_collection.export_collection_to_csv("dataset-ransomware-Domain", csv_header["Domain"], "Domain")
