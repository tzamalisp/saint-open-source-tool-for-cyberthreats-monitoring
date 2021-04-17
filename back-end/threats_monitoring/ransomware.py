from pymongo import MongoClient
from datetime import datetime
from bs4 import BeautifulSoup
import re
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

    crawling_time = datetime.utcnow()
    print("Report on", crawling_time.strftime('%Y-%m-%d %H:%M:%S'), '\n')

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
    print('Scraping finished')

    ''' Store instance of scraped data in MongoDB '''
    print("\nConnecting to MongoDB Data Base")
    db = connect_to_mongodb()

    db.threats.ransomware.drop()
    # import recent instance
    print("Storing Data...", end=' ')
    res = db.threats.ransomware.insert_many(total_list_data)

    print('Completed')
    print("\tDocuments Inserted: ", len(res.inserted_ids))
    # -----------------------------------------------------------------------------------------------------------------#

    """ Set Path Of Data Exportation """
    # set path of produced files
    path = '/var/www/html/saint/indicators2018/ransomware/'
    # -----------------------------------------------------------------------------------------------------------------#

    """ Descriptive Analysis and Result Exportation"""
    # Barplot Section
    query = {}
    projection = {"_id": 0}

    try:
        results_cursor = db.threats.ransomware.find(query, projection)
        # find last weeks top 10 countries and save them to csv and json. Specify name with NO EXTENSION
        top_entity_types = top_n(results_cursor, 3, 'Entity-Type', 'ransomware-top-entity-types', path)
        print("\nTop Ransomware Entity Types\n", top_entity_types)

        top_scope = top_n(results_cursor, 5, "Scope", 'ransomware-top-scope', path)
        print("\nTop Ransomware Scopes\n", top_scope)

        top_subcategories = top_n(results_cursor, 5, "Subcategory", "ransomware-top-subcategories", path)
        print("\nTop Ransomware Subcategories\n", top_subcategories)

    except Exception as e:
        print("__main__ > descriptive analysis phase > Barplot Analysis: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None
    # -----------------------------------------------------------------------------------------------------------------#

    """ Export Datasets """

    ransomware_csv_header = {
        "IP": ["Category", "Subcategory", "Entity-Type", "Scope", "IP", "False-Positive-Risk",
               "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI"],

        "URL": ["Category", "Subcategory", "Entity-Type", "Scope", "URL", "False-Positive-Risk",
                "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI"],

        "Domain": ["Category", "Subcategory", "Entity-Type", "Scope", "Domain", "False-Positive-Risk",
                   "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI"]
    }

    dataset_name_ip = 'dataset-ransomware-IP.csv'
    dataset_name_domain = 'dataset-ransomware-Domain.csv'
    dataset_name_url = 'dataset-ransomware-URL.csv'

    print("\nRetrieving MongoDB's Collection...")
    try:
        query_ip = {"Entity-Type": "IP"}
        query_domain = {"Entity-Type": "Domain"}
        query_url = {"Entity-Type": "URL"}
        projection = {"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0}

        results_cursor_ip = db.threats.ransomware.find(query_ip, projection)
        export_to_csv(results_cursor_ip, dataset_name_ip, ransomware_csv_header["IP"], path)

        results_cursor_domain = db.threats.ransomware.find(query_domain, projection)
        export_to_csv(results_cursor_domain, dataset_name_domain, ransomware_csv_header["Domain"], path)

        results_cursor_url = db.threats.ransomware.find(query_url, projection)
        export_to_csv(results_cursor_url, dataset_name_url, ransomware_csv_header["URL"], path)

    except Exception as e:
        print("__main__ > Export Datasets Phase: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None
