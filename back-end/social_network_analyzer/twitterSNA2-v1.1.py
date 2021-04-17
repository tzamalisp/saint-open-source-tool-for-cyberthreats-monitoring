import json
from nltk.tokenize import word_tokenize
import re
import operator
from collections import Counter
import string
from nltk.corpus import stopwords
from nltk import bigrams
import pandas as pd
import ijson


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', '…']


def get_mentions(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('user_mentions', [])
    return [tag['screen_name'] for tag in hashtags]



if __name__ == '__main__':


    fname = '/var/www/html/saint/twitterSNA-Aug17/data/stream__malware___ransomware___botnet___trojan.json'

    with open(fname, 'r') as f:
        countAllHashtags = Counter()
        countAllTerms = Counter()
        countAllMentions = Counter()

        # Dates list for storing the corresponding query in json file (see below)
        datesQuery = []

        for line in f:
            tweet = json.loads(line)

            if 'text' in tweet:
                # Create a list with all the terms
                terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
                terms_bigram = bigrams(terms_stop)
                # Count terms only once, equivalent to Document Frequency
                terms_single = set(terms_stop)
                # Count hashtags only
                terms_hash = [term for term in preprocess(tweet['text'])
                              if term.startswith('#')]
                # Count terms only (no hashtags, no mentions)
                terms_only = [term for term in preprocess(tweet['text'])
                              if term not in stop and
                              not term.startswith(('#', '@'))]
                # Count mentions only
                mentions_in_tweet = get_mentions(tweet)
                countAllMentions.update(mentions_in_tweet)
            # for user, count in countAllMentions.most_common(5):
            #     print("{}: {}".format(user, count))

                # mind the ((double brackets))
                # startswith() takes a tuple (not a list) if
                # we pass a list of inputs
                # Update the counter
                countAllHashtags.update(terms_hash)
                countAllTerms.update(terms_only)
                #countAllMentions = Counter(mentions_in_tweet)


                # track when the hashtag is mentioned
                if '#ransomware' in terms_hash:
                    datesQuery.append(tweet['created_at'])


        # Print the first 5 most frequent words
        print(countAllHashtags.most_common(5))
        print(countAllTerms.most_common(5))
        print(countAllMentions.most_common(5))


    """
    BARPLOT HASHTAGS
    """
    hash_freq = countAllHashtags.most_common(10)
    hash = pd.DataFrame(hash_freq)
    hash.set_index(0, inplace=True)
    hash.to_csv('/var/www/html/saint/twitterSNA-Aug17/hashesSNA2.csv')
    print('hash:')
    print(hash.head())


    """
    BARPLOT TERMS
    """
    terms_freq = countAllTerms.most_common(10)
    terms = pd.DataFrame(terms_freq)
    terms.set_index(0, inplace=True)
    terms.to_csv('/var/www/html/saint/twitterSNA-Aug17/termsSNA2.csv')
    print('terms:')
    print(terms.head())

    """
    BARPLOT USER MENTIONS
    """
    mentions_freq = countAllMentions.most_common(10)
    mentions = pd.DataFrame(mentions_freq)
    mentions.set_index(0, inplace=True)
    mentions.to_csv('/var/www/html/saint/twitterSNA-Aug17/mentionsSNA2.csv')
    print('mentions:')
    print(mentions.head())


    print()
    print()
    print('TIME SERIES')

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

    s.to_csv('/var/www/html/saint/twitterSNA-Aug17/perdayTimeSeries01SNA2.csv')