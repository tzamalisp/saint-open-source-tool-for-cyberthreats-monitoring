# general libraries
import time
from datetime import datetime
import pandas as pd

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


# MongoDB libraries

import pymongo
import json
from pymongo import MongoClient

import csv

print('phishtank is running....')


# connect to database
connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
db = connection.admin
db.authenticate('xxxxxx', 'xxxXXXxxxXX')
dbThreats = connection.threats

print("Database connection successful..")
print()



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



# parsing {0} to the string for iteration
indicator = 'https://www.phishtank.com/phish_search.php?page={0}&active=y&verified=u'

indicator1 = 'https://www.phishtank.com/phish_detail.php?phish_id=5489227'

indicator2 = 'http://httpstat.us/500'

indicator3 = 'https://www.meetup.com/'

indicator4 = 'https://hackerone.com/directory?query=type%3Ahackerone&sort=resolved_reports_closed%3Adescending&page=1'

indicator5 = 'https://www.phishtank.com/phish_search.php?page=300&active=y&verified=u'


# ----------------------------------------------------------------------------------------------------

# function for downloading web page
def download(url, num_retries=2, user_agent='giorgos93', charset='utf-8'):
    print('Downloading Page:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        html = urllib.request.urlopen(request).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                time.sleep(5)
                return download(url, num_retries - 1)
    return html

# ----------------------------------------------------------------------------------------------------

# function for getting ID links for further processing
def getLinks(html):
    # url = urllib.request.urlopen(html)
    soup = BeautifulSoup(html, 'html5lib')
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

# ----------------------------------------------------------------------------------------------------

# function for getting the content (exact Phish URL) from the ID page
def getContentItemID(url, num_retries=2, user_agent='giorgos94', charset='utf-8'):

    # print('Downloading Content:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)

    contentFromList = ''

    try:
        html = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(html, 'html5lib')

        # soupPretty = soup.prettify()
        #
        # pprint(soupPretty)

        valuesList = soup.find_all('b')

        if valuesList[1] != '':
            contentFromList = valuesList[1].text
        else:
            contentFromList = None

    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                time.sleep(5)
                return download(url, num_retries - 1)

    return contentFromList

# ----------------------------------------------------------------------------------------------------

# function for crawling the Phishtank website
def crawl_site(url, max_errors=5):

    print()

    num_errors = 0

    listBadLinks = []

    seenListBadLinks = set(listBadLinks)

    idIDs = []

    seenidIDs = set(idIDs)

    dictlistMongo = []

    for page in itertools.count(0):
        pg_url = url.format(page)
        html = download(pg_url)
        soup = BeautifulSoup(html, 'html5lib')
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
                    listBadLinks.append(getContentItemID(itemList))

            # print(listBadLinks)

            tree = fromstring(html)

            td = tree.cssselect('td.value')

            counter = 0

            for i in range(0, len(td), 5):

                # id
                id = td[i].text_content()
                id = int(id)

                idCheck = dbThreats.phishtank2.find_one({"_id": id})
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
                    dictionary['Phish URL'] = listBadLinks[counter]
                    dictionary['Submitted by'] = submittedFinal
                    dictionary['Valid?'] = valid
                    dictionary['Online?'] = online
                    dictionary['DatetimeUTC'] = datetimeUTC
                    dictionary['TimestampUTC'] = timestampUTC
                    dictionary['DatetimeUTC-CTI'] = datetimeUTCCTI
                    dictionary['TimestampUTC-CTI'] = timestampUTCCTI
                    dictionary['Entity type'] = 'URL'
                    dictionary['Category'] = 'Phishing'
                    # dictionary['mongoDate'] = datetimeObjectUTC

                    seenidIDs.add(id)
                    idIDs.append(id)
                    dictlistMongo.append(dictionary)

                    counter += 1

                time.sleep(0.5)

            # print(idIDs)
            # print(dictlistMongo)
            print('Length of list IDs:', len(seenidIDs))
            print('Length of Mongo Dictionary:', len(dictlistMongo))
            print('next')
            print()
            print()

        time.sleep(0.5)

    # drop collection if not empty
    if dbThreats.phishtank.count() != 0:
        dbThreats.phishtank.drop()
        print('Database reset')
    else:
        print('Database is empty! Starting storing data..')

    for dictionaryMongo in dictlistMongo:
        print(dictionaryMongo)
        # handle to web based attacks (1) collection
        phishtank = dbThreats.phishtank

        # Decode the JSON from Twitter
        jsonString = json.dumps(dictionaryMongo)
        datajson = json.loads(jsonString)

        # insert the data into the mongoDB into a collection called webBased
        # if twitter_search doesn't exist, it will be created.
        dbThreats.phishtank.insert(datajson)

    print()
    print("Data inserted successfully to MongoDB")
    print()
    print()
    print('The End!')


def timeSeriesAnalysis():

    # find the right collection
    phishtank = dbThreats.phishtank

    # if collection in not empty do:
    if phishtank.count() != 0:

        # Mongo Shell query
        # db.phishtank.find({}, {'DatetimeUTC': 1, '_id': 0})
        # print('yeah')

        query = {}
        # query = {'title': {'$regex': 'apple|google', '$options': 'i'}}
        projection = {'DatetimeUTC': 1, '_id': 0}
        # projection = {'title': 1, '_id': 0}
        try:
            cursor = phishtank.find(query, projection)
            # cursor = cursor.limit(10)

        except Exception as e:
            print("Unexpected error:", type(e), e)

        # Dates list for storing the corresponding query in json file (see below)
        datesQuery = []

        for doc in cursor:
            # print(doc['DatetimeUTC'])
            datesQuery.append(doc['DatetimeUTC'])


        """
        TIME SERIES
        """
        # a list of "1" to count the hashtags
        ones = [1] * len(datesQuery)
        # the index of the series
        idx = pd.DatetimeIndex(datesQuery)
        # print('idx:')
        # print(idx)
        # the actual series (at series of 1s for the moment)
        timeSeries01 = pd.Series(ones, index=idx)
        print(timeSeries01.head())

        # Resampling / bucketing
        per_day = timeSeries01.resample('1D').sum().fillna(0)

        print()
        print("Per Day:")
        print(per_day.head())

        s = pd.DataFrame(per_day)

        print(s.head())

        # s.to_csv('/var/www/html/saint/indicators2018/perdayTimeSeriesPhishtank.csv')

        s.to_csv('/var/www/html/saint/indicators2018/phishing/perdayTimeSeriesPhishtank.csv')

    else:
        print('Database is empty! Can not retrieve data!')

    print()

# ----------------------------------------------------------------------------------------------------


def csvToJson():

    jsonPhishtank = []

    with open('/var/www/html/saint/indicators2018/phishing/perdayTimeSeriesPhishtank.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            row[0] = row[0] + ' 14:00:00.000'
            datetimeObject = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            millisec = datetimeObject.timestamp() * 1000
            row[0] = millisec
            row[1] = int(float(row[1]))
            print(row)
            jsonPhishtank.append(row)

    del jsonPhishtank[0]

    print()
    print('new file:')
    print(jsonPhishtank)

    print()
    print('Writing..')
    with open('/var/www/html/saint/indicators2018/phishing/phishtankjson.json', 'w') as file:
        json.dump(jsonPhishtank, file, indent=4)

    print('Writing complete!')

if __name__ == '__main__':

    crawl_site(indicator)

    # print(getContentItemID(indicator1))

    # print(download(indicator1))

    # getPageTableValues(indicator)

    timeSeriesAnalysis()
    csvToJson()
