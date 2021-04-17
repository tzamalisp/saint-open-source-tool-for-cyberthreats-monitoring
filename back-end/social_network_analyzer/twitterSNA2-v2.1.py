from pymongo import MongoClient
import pandas as pd
from collections import Counter

# NLP libraries
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
import csv
import json
# from datetime import datetime
import datetime
from collections import deque
import pymongo


"""TIME SERIES DESCRIPTIVE ANALYSIS SECTION"""

"""TIME SERIES DESCRIPTIVE ANALYSIS - RANSOMWARE HASHTAGS"""
# Function for Data Analysis and CSV file creation
def findHashtagsTimeSeriesRansomware():

    print("Finding tweets with #ransomware hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"ransomware",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    query = {'entities.hashtags.text': {'$regex':'ransomware','$options': 'i'}}
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

    print('Writing CSV file for time series analysis of tweets with Ransomware hashtags')
    s.to_csv('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesRansomware.csv')
    print('Writing Ransomware Time Series Descriptive Analysis CSV file completed!')


# function for converting CSV to JSON
def csvToJsonRansomware():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesRansomware.csv') as csvfile:
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
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesRansomware.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Ransomware JSON file completed!')
    print()
    print('Next:')



"""TIME SERIES DESCRIPTIVE ANALYSIS - MALWARE HASHTAGS"""
# Function for Data Analysis and CSV file creation
def findHashtagsTimeSeriesMalware():

    print("Finding tweets with #malware hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"malware",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    query = {'entities.hashtags.text': {'$regex': 'malware', '$options': 'i'}}
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

    print('Writing CSV file for time series analysis of tweets with Malware hashtags')
    s.to_csv('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesMalware.csv')
    print('Writing Malware Time Series Descriptive Analysis CSV file completed!')


# function for converting CSV to JSON
def csvToJsonMalware():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesMalware.csv') as csvfile:
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
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesMalware.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Malware JSON file completed!')
    print()
    print('Next:')



"""TIME SERIES DESCRIPTIVE ANALYSIS - TROJAN HASHTAGS"""
# Function for Data Analysis and CSV file creation
def findHashtagsTimeSeriesTrojan():

    print("Finding tweets with #trojan hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"trojan",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    query = {'entities.hashtags.text': {'$regex': 'trojan', '$options': 'i'}}
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
    s.to_csv('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesTrojan.csv')
    print('Writing Trojan Time Series Descriptive Analysis CSV file completed!')

# function for converting CSV to JSON
def csvToJsonTrojan():
    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesTrojan.csv') as csvfile:
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
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesTrojan.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Trojan JSON file completed!')
    print()
    print('Next:')


"""TIME SERIES DESCRIPTIVE ANALYSIS - BOTNET HASHTAGS"""
# Function for Data Analysis and CSV file creation
def findHashtagsTimeSeriesBotnet():

    print("Finding tweets with #botnet hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"botnet",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    query = {'entities.hashtags.text': {'$regex': 'botnet', '$options': 'i'}}
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
    s.to_csv('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesBotnet.csv')
    print('Writing Botnet Time Series Descriptive Analysis CSV file completed!')

# function for converting CSV to JSON
def csvToJsonBotnet():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesBotnet.csv') as csvfile:
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
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesBotnet.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Botnet JSON file completed!')
    print()
    print('Next:')



"""TIME SERIES DESCRIPTIVE ANALYSIS - PHISHING HASHTAGS"""
# Function for Data Analysis and CSV file creation
def findHashtagsTimeSeriesPhishing():

    print("Finding tweets with #phishing hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"phishing",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    query = {'entities.hashtags.text': {'$regex': 'phishing', '$options': 'i'}}
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
    s.to_csv('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesPhishing.csv')
    print('Writing Botnet Time Series Descriptive Analysis CSV file completed!')

# function for converting CSV to JSON
def csvToJsonPhishing():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesPhishing.csv') as csvfile:
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
    with open('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeriesPhishing.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Botnet JSON file completed!')
    print()
    print('Next:')


"""CATEGORICAL ANALYSIS SECTION"""

"""CATEGORICAL ANALYSIS - MOST FREQUENT HASHTAGS"""
# Function for Categorical Analysis and CSV file creation
def findMostFrequentHashtags():

    print("Finding tweets with included hashtags from the Database, over the last 7 days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    sevenDaysAgo = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$exists : true}}, {'entities.hashtags.text': 1, '_id': 0}).limit(5)

    # creating query + projection for MongoDB
    query = {'$and': [{'entities.hashtags.text': {'$exists': 'true'}}, {'mongoDate': {'$gte': sevenDaysAgo}}]}
    projection = {'entities.hashtags.text': 1, '_id': 0}

    # running query
    cursor = []
    try:
        cursor = twitterOutput2.find(query, projection)
        # cursor = cursor.limit(20)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    print("Finding used hashtags frequency..")
    # Listing countered hashtags coming from tweets for storing later the corresponding query in a CSV file
    countAllHashtags = Counter()
    hashtagsList = []
    for doc in cursor:
        hashtagsKey = doc['entities']['hashtags']
        for item in hashtagsKey:
            # print(item['text'])
            hashtagsList.append(('#' + item['text'].lower()))
            # countAllHashtags.update(item['text'])

    # print(hashtagsList)
    countAllHashtags.update(hashtagsList)

    print('Most 10 frequently used hashtags:')
    print(countAllHashtags.most_common(10))

    """
    CATEGORICAL ANALYSIS (BAR-PLOT) PANDAS SECTION
    """
    hash_freq = countAllHashtags.most_common(10)
    hash = pd.DataFrame(hash_freq)
    hash.set_index(0, inplace=True)
    print('Data frame:')
    print(hash.head())
    hash.to_csv('/var/www/html/saint/twitterSNA-Aug17/hashtagsThreats.csv')
    print('Writing Hashtags Categorical Analysis to CSV file completed!')


def csvToJsonHashtags():
    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonBarPlotsHashtags = []
    with open('/var/www/html/saint/twitterSNA-Aug17/hashtagsThreats.csv') as csvfileHash:
        readCSVHash = csv.reader(csvfileHash, delimiter=',')
        next(readCSVHash)
        for row in readCSVHash:
            row[1] = int(row[1])
            jsonBarPlotsHashtags.append(row)

    # print('new file Hashtags Bar Plots:')
    # print(jsonBarPlotsHashtags)
    print('Writing JSON file..')
    with open('/var/www/html/saint/twitterSNA-Aug17/hashtagsThreats.json', 'w') as file:
        json.dump(jsonBarPlotsHashtags, file, indent=4)
    print('Writing Hashtags Bar-Plots JSON file completed!')
    print()
    print('Next:')


"""CATEGORICAL ANALYSIS - MOST FREQUENT MENTIONS"""
def findMostFrequentMentions():

    print("Finding tweets with included mentions from the Database, over the last 7 days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    sevenDaysAgo = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.user_mentions.screen_name': {$exists : true}}, {'entities.user_mentions.screen_name': 1, '_id': 0}).limit(5)

    # creating query + projection for MongoDB
    query = {'$and': [{'entities.user_mentions.screen_name': {'$exists' : 'true'}}, {'mongoDate': {'$gte': sevenDaysAgo}}]}
    projection = {'entities.user_mentions.screen_name': 1, '_id': 0}


    # running query
    cursor = []
    try:
        cursor = twitterOutput2.find(query, projection)
        # cursor = cursor.limit(20)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    print("Finding used mentions frequency..")
    # Listing countered mentions coming from tweets for storing later the corresponding query in a CSV file
    countAllMentions = Counter()
    mentionsList = []
    for doc in cursor:
        screenNameKey = doc['entities']['user_mentions']
        for item in screenNameKey:
            # print(item['screen_name'])
            mentionsList.append(item['screen_name'])
            # countAllMentions.update(item['screen_name'])

    # print(mentionsList)
    countAllMentions.update(mentionsList)

    print('Most 10 frequently used mentions:')
    print(countAllMentions.most_common(5))

    """
        CATEGORICAL ANALYSIS (BAR-PLOT) PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating data frame:')
    mentions_freq = countAllMentions.most_common(10)
    mentions = pd.DataFrame(mentions_freq)
    mentions.set_index(0, inplace=True)
    print('Data frame:')
    print(mentions.head())
    mentions.to_csv('/var/www/html/saint/twitterSNA-Aug17/mentionsThreats.csv')
    print('Writing Mentions Categorical Analysis to CSV file completed!')

def csvToJsonMentions():
    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonBarPlotsMentions = []
    with open('/var/www/html/saint/twitterSNA-Aug17/mentionsThreats.csv') as csvfileMentions:
        readCSVMentions = csv.reader(csvfileMentions, delimiter=',')
        next(readCSVMentions)
        for row in readCSVMentions:
            row[1] = int(row[1])
            jsonBarPlotsMentions.append(row)

    # print('New file --> Mentions Bar-Plots:')
    # print(jsonBarPlotsMentions)
    print('Writing JSON file..')
    with open('/var/www/html/saint/twitterSNA-Aug17/mentionsThreats.json', 'w') as file:
        json.dump(jsonBarPlotsMentions, file, indent=4)
    print('Writing Mentions Bar-Plots JSON file completed!')
    print()
    print('Next:')



"""CATEGORICAL ANALYSIS - MOST FREQUENT TERMS"""
# function for tweet processing
def process(text, tokenizer=TweetTokenizer(), stopwords=[]):
    """Process the text of a tweet:
        1. Lowercase
        2. Tokenize
        3. Stopword removal
        4. Digits removal
        5. Return list
    """
    textLowercase = text.lower()
    tokens = tokenizer.tokenize(textLowercase)

    return [tok for tok in tokens if tok not in stopwords and not tok.isdigit() and not tok.startswith(('#', '@', 'http', 'https'))]


# function for splitting contracted forms of two separate tokens
def normalize_contractions(tokens):
    token_map = {
        "i'm": "i am",
        "you're": "you are",
        "it's": "it is",
        "we're": "we are",
        "we'll": "we will",
    }
    for tok in tokens:
        if tok in token_map.keys():
            for item in token_map[tok].split():
                yield item
        else:
            yield tok


# Function for Categorical Analysis and CSV file creation
def findMostFrequentTerms():

    print("Finding tweets with included terms from the Database, over the last 7 days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    sevenDaysAgo = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    # creating query + projection for MongoDB
    query = {'$and': [{'text': {'$exists': 'true'}}, {'mongoDate': {'$gte': sevenDaysAgo}}]}
    projection = {'text': 1, 'created_at': 1, '_id': 0}

    # running query
    cursor = []
    try:
        cursor = twitterOutput2.find(query, projection)
        # cursor = cursor.limit(50)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    print("Finding used terms frequency..")
    # Listing countered terms coming from tweets for storing later the corresponding query in a CSV file
    termsList = []
    countAllTerms = Counter()
    tweetTokenizer = TweetTokenizer()
    punct = list(string.punctuation)
    stopwordList = stopwords.words('english') + punct + ['rt', 'via', '…', '...', '..', 'yang', "i'm",
                                                         'one', 'like', 'de', 'la', 'le', 'les', 'et', 'que', 'en',
                                                         'qui', 'un', 'des', 'pour', 'une', 'ce', 'pas', 'avec',
                                                         'est', 'sur', 'se', 'du', 'dans', 'el', "c'est", "don't",
                                                         'vous', 'il', 'di', 'ne', 'sont', 'fs', 'au', 'aku', 'dan',
                                                         'love', 'yg', 'ada', 'tidak', 'dm', 'ya', 'es', 'kamu',
                                                         'lebih', 'son', 'par', 'naruto', 'jika', 'kau', 'dia', 'te',
                                                         'ft', 'dari', 'bisa', 'f', 'v', 'ou', 'al', 'una', 'im',
                                                         "i'll", 'con', 'tu', 'zaif', 'apa', 'us', 'pada', 'mau',
                                                         'ou', 'oh', 'e', 'u', 'si', 'itu', "you're", "you re", 'ga',
                                                         'je', 'las', 'b', 'h', 'die', 'ini', 'ont', 'c', 'l', 'r',
                                                         'jangan', 'akan', ':/', 'karena', 'dont', 'ass', 'kita',
                                                         'tak', "that's", 'untuk', 'dalam', 'lagi', 'it', 'adalah',
                                                         'orang', 'visit', "can't", 'cant', 'know', "it's", 'get',
                                                         'burp', 'jenkins', 'using', 'time', 'epic', 'every', 'chance',
                                                         'win', 'box', 'condoms', 'condom', 'mens', 'shot', 'new',
                                                         'sex', 'shots', 'cum', 'hi', 'vs', 'boyz', 'coming', 'break',
                                                         'music', 'video', 'generations', 'ballistik']

    for doc in cursor:
        tokens = ''
        doc['text'] = doc['text'].encode('ascii', 'ignore')
        # print(doc['text'])
        try:
            tokens = process(text=doc['text'], tokenizer=tweetTokenizer, stopwords=stopwordList)
            # print(tokens)
        except Exception as exceptionTweet:
            print('Error! Not valid term:', exceptionTweet)

        countAllTerms.update(tokens)

    print('Most 10 frequently used terms:')
    print(countAllTerms.most_common(10))

    """
        CATEGORICAL ANALYSIS (BAR-PLOT) PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating data frame:')
    terms_freq = countAllTerms.most_common(10)
    terms = pd.DataFrame(terms_freq)
    terms.set_index(0, inplace=True)
    print('Data frame:')
    print(terms.head())
    terms.to_csv('/var/www/html/saint/twitterSNA-Aug17/termsThreats.csv')
    print('Writing Terms Categorical Analysis to CSV file completed!')

# function for converting CSV to JSON
def csvToJsonTerms():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonBarPlotsTerms = []
    with open('/var/www/html/saint/twitterSNA-Aug17/termsThreats.csv') as csvfileTerms:
        readCSVTerms = csv.reader(csvfileTerms, delimiter=',')
        next(readCSVTerms)
        for row in readCSVTerms:
            row[1] = int(row[1])
            jsonBarPlotsTerms.append(row)

    # print('New file --> Terms Bar-Plots:')
    # print(jsonBarPlotsTerms)
    print('Writing JSON file..')
    with open('/var/www/html/saint/twitterSNA-Aug17/termsThreats.json', 'w') as file:
        json.dump(jsonBarPlotsTerms, file, indent=4)
    print('Writing Terms Bar Plots to JSON file completed!')


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
    print('TIME SERIES DESCRIPTIVE ANALYSIS - RANSOMWARE HASHTAGS')
    findHashtagsTimeSeriesRansomware()
    csvToJsonRansomware()
    print()
    print('TIME SERIES DESCRIPTIVE ANALYSIS - MALWARE HASHTAGS')
    findHashtagsTimeSeriesMalware()
    csvToJsonMalware()
    print()
    print('TIME SERIES DESCRIPTIVE ANALYSIS - TROJAN HASHTAGS')
    findHashtagsTimeSeriesTrojan()
    csvToJsonTrojan()
    print()
    print('TIME SERIES DESCRIPTIVE ANALYSIS - BOTNET HASHTAGS')
    findHashtagsTimeSeriesBotnet()
    csvToJsonBotnet()
    print()
    print('TIME SERIES DESCRIPTIVE ANALYSIS - PHISHING HASHTAGS')
    findHashtagsTimeSeriesPhishing()
    csvToJsonPhishing()
    print()
    # print('CATEGORICAL ANALYSIS - MOST FREQUENT HASHTAGS')
    # findMostFrequentHashtags()
    # csvToJsonHashtags()
    # print()
    # print('CATEGORICAL ANALYSIS - MOST FREQUENT MENTIONS')
    # findMostFrequentMentions()
    # csvToJsonMentions()
    # print()
    # print('CATEGORICAL ANALYSIS - MOST FREQUENT TERMS')
    # findMostFrequentTerms()
    # csvToJsonTerms()

    print('Process Completed!')

