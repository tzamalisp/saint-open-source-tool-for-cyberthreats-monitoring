from pymongo import MongoClient
import pandas as pd
from collections import Counter
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# NLP libraries
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
import csv
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# from datetime import datetime
import datetime
from collections import deque
import pymongo


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

    print("Finding tweets with included terms from the Database, over the last X days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    daycounter = datetime.datetime.utcnow() - datetime.timedelta(days=30)

    # creating query + projection for MongoDB
    query = {'$and': [{'text': {'$exists': 'true'}}, {'mongoDate': {'$gte': daycounter}}]}
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
                                                         'burp', 'jenkins', 'using', 'time']

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
    print()
    print('Creating Wordcloud..')
    wordcloud = WordCloud(width=2048, height=1080, background_color='white').generate_from_frequencies(countAllTerms)

    print(wordcloud)
    fig2 = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    fig2.savefig("/var/www/html/saint/twitterSNA-Aug17/wordcloud/wordThreats.png", dpi=900)
    plt.close()
    print('Wordcloud generated successfully')
    print()

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
    terms.to_csv('/var/www/html/saint/twitterSNA-Aug17/wordcloud/wordThreats.csv')
    print('Writing Terms Categorical Analysis to CSV file completed!')

# function for converting CSV to JSON
def csvToJsonTerms():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonBarPlotsTerms = []
    with open('/var/www/html/saint/twitterSNA-Aug17/wordcloud/wordThreats.csv') as csvfileTerms:
        readCSVTerms = csv.reader(csvfileTerms, delimiter=',')
        next(readCSVTerms)
        for row in readCSVTerms:
            row[1] = int(row[1])
            jsonBarPlotsTerms.append(row)

    # print('New file --> Terms Bar-Plots:')
    # print(jsonBarPlotsTerms)
    print('Writing JSON file..')
    with open('/var/www/html/saint/twitterSNA-Aug17/wordcloud/wordThreats.json', 'w') as file:
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
    print('CATEGORICAL ANALYSIS - MOST FREQUENT TERMS')
    findMostFrequentTerms()
    csvToJsonTerms()

    print('Process Completed!')

