from pymongo import MongoClient
import pandas as pd
from collections import Counter
from pprint import pprint

# NLP libraries
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
import csv
import json
# from datetime import datetime
import datetime
from collections import deque
import re


"""TIME SERIES DESCRIPTIVE ANALYSIS - TERMS FROM JSON"""
# Function for Data Analysis and CSV file creation
def findTermsTimeSeries(term):
    print('Term for search in Database:', term)
    print("Finding tweets with  specific term from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'text': {$regex: 'malware', $options: 'i'}}, {'_id': 0, 'created_at': 1})

    # creating query + projection for MongoDB
    # query = {'text': {'$regex': term, '$options': 'i'}}
    query = {'text': re.compile(term, re.IGNORECASE)}
    projection = {'created_at': 1, '_id': 0}

    # running query
    try:
        cursor = twitterOutput2.find(query, projection)
        # cursor = cursor.limit(2)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    # Listing dates coming from tweets for storing later the corresponding query in a CSV file
    datesQuery = []
    for doc in cursor:
        # print(doc['created_at'])
        datesQuery.append(doc['created_at'])

    print('Number of tweets that include this term:', len(datesQuery))

    print()

    """
            TIME SERIES ANALYSIS PANDAS SECTION
        """
    print('Starting data analysis with Pandas.')
    print('Creating Time Series:')
    # a list of "1" to count the hashtags
    ones = [1] * len(datesQuery)
    # the index of the series
    idx = pd.DatetimeIndex(datesQuery)
    # print('idx:')
    # print(idx)
    # the actual series (at series of 1s for the moment)
    timeSeries01 = pd.Series(ones, index=idx)
    print(timeSeries01.head())
    print("Counting tweets per day - executing descriptive analysis - Re-sampling / Bucketing..")
    # Resampling / bucketing
    per_day = timeSeries01.resample('1D').sum().fillna(0)
    print('Time Series created:')
    print(per_day.head())
    print('Creating data frame..')
    s = pd.DataFrame(per_day)
    print('Data frame:')
    print(s.head())

    print('Writing CSV file..')
    s.to_csv('/var/www/html/saint/twitterSNA-Aug17/sna-feed/ransomware/feedPerDayTimeSeriesRansomware' + term + '.csv')
    print('Writing ' + term + ' Time Series Descriptive Analysis CSV file completed!')

    return term

# function for converting CSV to JSON
def csvToJson(term2):
    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/var/www/html/saint/twitterSNA-Aug17/sna-feed/ransomware/feedPerDayTimeSeriesRansomware' + term2 + '.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            row[0] = row[0] + ' 14:00:00.000'
            datetimeObject = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            millisec = datetimeObject.timestamp() * 1000
            row[0] = millisec
            row[1] = int(float(row[1]))
            # print(row)
            jsonTimeSeries.append(row)
    # removing the head (first object) with not useful data - Data cleaning
    del jsonTimeSeries[0]

    # print('New file --> Time Series:')
    # print(jsonTimeSeries)
    print('Writing JSON file..')
    with open('/var/www/html/saint/twitterSNA-Aug17/sna-feed/ransomware/feedPerDayTimeSeriesRansomware' + term2 + '.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Trojan JSON file completed!')

"""MAIN FUNCTION"""
if __name__ == '__main__':

    # current Datetime the process is running
    now = datetime.datetime.now()
    print('Time now:', now)

    utcnow = datetime.datetime.utcnow()
    print('Time now in UTC:', utcnow)

    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    # find the db
    twitterDB = connection.twitter

    # find the right collection
    twitterOutput2 = twitterDB.twitterQuery2

    print("Database connection successful..")
    print()

    with open('/var/www/html/saint/indicators2018/ransomware/ransomware-top-subcategories.json') as f:
        data = json.load(f)

    pprint(data)

    print('Data inserted to variable successfully')
    print()
    print()

    counter = 0
    for i in data:
        print('KEYWORD PROCESS:')
        csvToJson(findTermsTimeSeries(data[counter][0].lower()))
        counter += 1
        print()

    print()
    print()
    print('PROCESS FINISHED SUCCESSFULLY!')



