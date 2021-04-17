import time
from datetime import datetime
import pandas as pd
import lxml

# crawling libraries
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
import itertools

# scraping libraries
from bs4 import BeautifulSoup
from lxml.html import fromstring, tostring
import re
import cssselect
from pprint import pprint

from pymongo import MongoClient
from downloader import Downloader
import json
import  csv
import os


# to run on server
server_path = '/var/www/html/saint/indicators2018/phishing/'
# to run locally
# server_path = ""
print("Report on", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '\n')

# getting timestamp in UTC in Microsecond accuracy
print("Time in UTC:")
ts = datetime.utcnow().timestamp()
print(ts)
valueDt = datetime.fromtimestamp(ts)
dateTimeMongo = valueDt.strftime('%Y-%m-%d %H:%M:%S')
print(valueDt)
dateTimeMongoUTC = datetime.utcnow()
print(dateTimeMongoUTC)
print()


# -------------------------------------------------------------------------------------------------------------------- #
def connect_to_mongodb():
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    return db


# -------------------------------------------------------------------------------------------------------------------- #


def getLinks(html):
    """ This function downloads a web page and discovers all it's links
        @param
            html        (string)    webpage 's html code
        @return
            htmlLinks   (list)      contains all the discovers links
    """

    soup = BeautifulSoup(html, 'lxml')
    possible_links = soup.find_all('a')

    htmlLinks = []

    for link in possible_links:
        if link.has_attr('href'):
            if link.attrs['href'].startswith("phish_detail.php?phish_id="):
                linkDefault = 'https://www.phishtank.com/'
                linkConnect = '{}{}'.format(linkDefault, link.attrs['href'])
                htmlLinks.append(linkConnect)
                #print(link.attrs['href'])

    return htmlLinks


# -------------------------------------------------------------------------------------------------------------------- #


def getContentItemID(url, downloader):
    """ This function receives the url of a specific phish page (ID), then finds and returns it's http host link
        @param
            url     (str)   url page of a phish attack
        @return
            contentFromList  (str)  the host page of phish attack
    """

    html = downloader(url)
    # parse html
    soup = BeautifulSoup(html, 'lxml')
    # studying the page revealed that the phish url is in bold
    valuesList = soup.find_all('b')

    if valuesList[1] != '':
        contentFromList = valuesList[1].text
    else:
        contentFromList = None


    return contentFromList


# -------------------------------------------------------------------------------------------------------------------- #


def crawl_site(db, url, max_errors=5):
    """ This is the main function for crawling Phishtank website
        @param
            db
            url
            max_errors
        @return:
    """

    num_errors = 0
    listBadLinks = []
    seenListBadLinks = set(listBadLinks)
    idIDs = []
    seenidIDs = set(idIDs)
    dictlistMongo = []

    downloader =  Downloader(delay=1,  user_agent='giorgos93', cache={})

    for page in itertools.count(0):
        pg_url = url.format(page)
        # prepare Downloader object

        # download a page
        html = downloader(pg_url)
        # parse page
        soup = BeautifulSoup(html, 'lxml')
        td = soup.find_all(attrs={'class': 'value'})

        if not td:
            print('no tables!')
            num_errors += 1
            if num_errors == max_errors:
                # reached max number of errors, so exit
                break
        elif html is None:
            num_errors += 1
            if num_errors == max_errors:
                # reached max number of errors, so exit
                break
        else:
            num_errors = 0
            # success - can scrape the result
            # CSS Selectors - XPATH
            print()
            print('Content:')

            listGetContentIDs = getLinks(html)
            # print('List with ID links')
            # print(listGetContentIDs)
            print()

            for itemList in listGetContentIDs:
                if itemList not in seenListBadLinks:
                    seenListBadLinks.add(itemList)
                    listBadLinks.append(getContentItemID(itemList, downloader))

            tree = fromstring(html)
            td = tree.cssselect('td.value')
            counter = 0

            for i in range(0, len(td), 5):
                # id
                id = td[i].text_content()
                id = int(id)

                idCheck = db.threats.phishtank.find_one({"_id": id})
                # print(idCheck)

                if idCheck is None:
                    print('Not duplicate key found! Continue..')
                else:
                    print('Duplicate key value found:', idCheck['_id'])

                # datetime
                date = td[i + 1].text_content()
                date2 = date.split()
                del date2[0:2]
                dataClean = date2[1]
                s1 = []
                for s in dataClean:
                    if s.isdigit():
                        s1.append(s)
                dataClean2 = ''.join(s1)
                date2[1] = dataClean2
                dataCleanFinal = ' '.join(date2)
                print(dataCleanFinal)

                try:
                    # valid_date = time.strptime(date, '%m/%d/%Y')
                    datetimeObjectUTC = datetime.strptime(dataCleanFinal, '%b %d %Y %I:%M %p')
                    print('datetimeObjectUTC:', datetimeObjectUTC)
                except ValueError:
                    print('Invalid date!')

                # datetimeObjectUTC = datetime.strptime(dataCleanFinal, '%b %d %Y %I:%M %p')
                datetimeUTC = datetimeObjectUTC.strftime('%Y-%m-%d %H:%M:%S')
                print('datetimeUTC:', datetimeUTC)
                timestampUTC = int(time.mktime(datetimeObjectUTC.timetuple()))

                # CTI datetime
                datetimeObjectUTCCTI = dateTimeMongoUTC
                datetimeUTCCTI = datetimeObjectUTCCTI.strftime('%Y-%m-%d %H:%M:%S')

                # CTI timestamp
                timestampUTCCTI = ts

                # author
                submitted = td[i + 2].text_content()
                if submitted != '':
                    submitted2 = submitted.split()
                    submittedFinal = submitted2[1]
                else:
                    submittedFinal = None

                # valid
                valid = td[i + 3].text_content()
                if valid == '':
                    valid = None

                # online
                online = td[i + 4].text_content()
                if online == '':
                    online = None

                # print(datetimeUTC)

                dictionary = {}

                if id not in seenidIDs:

                    dictionary['_id'] = id
                    dictionary['Phish-URL'] = listBadLinks[counter]
                    dictionary['Submitted-by'] = submittedFinal
                    dictionary['Valid?'] = valid
                    dictionary['Online?'] = online
                    dictionary['TimestampUTC'] = timestampUTC
                    dictionary["mongoDate"] = datetimeObjectUTC
                    dictionary['DatetimeUTC'] = datetimeUTC
                    dictionary['TimestampUTC-CTI'] = timestampUTCCTI
                    dictionary['mongoDate-CTI'] = datetimeObjectUTCCTI
                    dictionary['DatetimeUTC-CTI'] = datetimeUTCCTI
                    dictionary['Entity-type'] = 'URL'
                    dictionary['Category'] = 'Phishing'

                    seenidIDs.add(id)
                    idIDs.append(id)
                    dictlistMongo.append(dictionary)

                    counter += 1

                # TODO: delete time.sleep()
                # time.sleep(0.5)

            print('Length of list IDs:', len(seenidIDs))
            print('Length of Mongo Dictionary:', len(dictlistMongo))
            print('next')
            print()
            print()

        # time.sleep(0.5)

    # drop collection if not empty
    if db.threats.phishtank.count() != 0:
        db.threats.phishtank.drop()
        print('Database reset')
    else:
        print('Database is empty! Starting storing data..')

    for dictionaryMongo in dictlistMongo:
        print(dictionaryMongo)
        # handle to web based attacks (1) collection
        # phishtank = db.threats.phishtank

        db.threats.phishtank.insert(dictionaryMongo)

    print()
    print("Data inserted successfully to MongoDB")
    print()
    print()
    print('The End!')


    # ---------------------------------------------------------------------------------------------------------------- #


def data_frame_to_json(data_frame, filename):
    """ Given a data_frame creates a list of smaller lists that contain data frame pairs and stores them in a json file
        @param
            data_frame
            filename:   (str)   the name of the json file to be created
    """

    data_frame_list = list([])
    # break down every data frame row in tuple
    for row in data_frame.itertuples():
        # then keep the necessary stuff, the index timestamp and the accumulated value
        timestamp = high_charts_timestamp(row[0])
        row_list = [timestamp, row[1]]
        # append each list in an other list
        data_frame_list.append(row_list)
    # save list of lists in the file
    with open(filename, 'w') as json_file:
        json.dump(data_frame_list, json_file, indent=4)


# ---------------------------------------------------------------------------------------------------------------------#


def high_charts_timestamp(datetime_obj):
    """ This is a post processing function. It receives a pandas datetime element and takes care of producing
        a timestamp suitable for high charts
        @param
            datetime_obj            (datetime)
        @returns
            high_charts_timestamp   (timestamp)     readable by high charts
    """

    # due to pandas processing the datetime_oj have always the structure xx:xx:xx 00:00:00 format
    # so retrieving year, month, day is all we need to begin converting

    datetime_obj_tuple = datetime_obj.timetuple()
    year = datetime_obj_tuple.tm_year
    month = datetime_obj_tuple.tm_mon
    day = datetime_obj_tuple.tm_mday
    # string
    high_charts_datetime_string = datetime(year, month, day, 14, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S.%f')
    # datetime
    high_charts_datetime_obj = datetime.strptime(high_charts_datetime_string, '%Y-%m-%d %H:%M:%S.%f')
    high_charts_timestamp = high_charts_datetime_obj.timestamp() * 1000

    return high_charts_timestamp


# ---------------------------------------------------------------------------------------------------------------------#


def time_series_analysis(db):
    """ Collects all the information from the collection and presents the number of blocked IP's per day
        Saves the results in csv and json file respectively for later process (stakeholders and Highcharts)
        @param
            db:     (Mongo Client)  this is the connection returned by Pymongo Client,
                                    we take it from connect_to_mongodb() function
    """

    num_of_docs_in_collection = db.threats.phishtank.count()

    # Process Data if the collection is not empty
    if num_of_docs_in_collection != 0:
        try:
            # retrieve DatetimeUTC for all docs in collection
            cursor = db.threats.phishtank.find({}, {'mongoDate': 1, '_id': 0})
            # Dates list for storing the corresponding query in json file
            dates_list = list([])
            for doc in cursor:
                dates_list.append(doc['mongoDate'])
            ''' Time Series '''
            # a list of "1" to count the docs
            ones = [1] * len(dates_list)
            # the index of the series
            idx = pd.DatetimeIndex(dates_list)
            # the actual series (at series of 1s for the moment)
            time_series = pd.Series(ones, index=idx)
            print(time_series.head())

            # Resampling / bucketing
            per_day = time_series.resample('1D').sum().fillna(0)

            print("Per Day:")
            print(per_day.head())

            print("\nDataFrame per Day")
            s = pd.DataFrame(per_day)
            print(s.head())

            s.to_csv(server_path + 'perdayTimeSeriesPhishtank.csv')
            data_frame_to_json(s, server_path + 'phishtankjson.json')

        except Exception as e:
            print("Unexpected error:", type(e), e)

    else:
        print('Database is empty! Can not retrieve data!')


# ---------------------------------------------------------------------------------------------------------------------#


def extract_collection_copy(db):
    """ For a given data base, retrieves all data from a collection and export them in json and csv files
        @param
            db:     (Mongo Client)  this is the connection returned by Pymongo Client,
                                    we take it from connect_to_mongodb() function
    """

    json_filename = server_path + 'dataset-phishing.json'
    csv_filename = server_path + 'dataset-phishing.csv'
    try:
        cursor = db.threats.phishtank.find({}, {"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0})

        ''' Store in json file '''
        # add a bracket [ and start inserting docs in json file
        with open(json_filename, 'w') as json_file:
            json_file.write('[\n')
            for doc in cursor:
                json.dump(doc, json_file, separators=(',', ': '), indent=4)
                json_file.write(',\n')
        # delete last comma and new line
        with open(json_filename, 'ab+') as json_file:
            json_file.seek(-3, os.SEEK_END)  # puts cursor's position over the last character of the file
            # delete last \n
            json_file.truncate()
        # insert bracket ] for a valid json
        with open(json_filename, 'a') as json_file:
            json_file.write('\n]')

        ''' Store in csv file '''
        with open(csv_filename, "w", newline='') as csvfile:
            csv_header = ["Phish-URL", "Submitted-by", "Valid?", "Online?", "DatetimeUTC", "TimestampUTC",
                          "DatetimeUTC-CTI", "TimestampUTC-CTI", "Entity-type", "Category"]
            writer = csv.DictWriter(csvfile, fieldnames=csv_header)
            writer.writeheader()
            for doc in cursor.rewind():
                writer.writerow(doc)

    except Exception as e:
            print("Unexpected error (collection export):", type(e), e)


# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":

    # parsing {0} to the string for iteration
    indicator = 'https://www.phishtank.com/phish_search.php?page={0}&active=y&verified=u'

    ''' Connect to mongoDB '''
    db = connect_to_mongodb()

    ''' Crawl Phishtank'''
    crawl_site(db, indicator)

    ''' Descriptive time series processing '''
    # db is passed to retrieve docs from MongoDB
    time_series_analysis(db)

    ''' Export current MongoDB instance '''
    extract_collection_copy(db)
