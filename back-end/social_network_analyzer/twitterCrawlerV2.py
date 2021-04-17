
# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python3 twitterCrawlerV1.py -q google -d data
# 
# It will produce the list of tweets for the query "google" 
# in the file data/stream_google.json

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import pymongo
import datetime

from pymongo import MongoClient

# def get_parser():
#     """Get parser for command line arguments."""
#     parser = argparse.ArgumentParser(description="Twitter Downloader")
#     parser.add_argument("-q",
#                         "--query",
#                         dest="query",
#                         help="Query/Filter",
#                         default='-')
#     return parser

class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def on_data(self, data):
        try:
            print('Raw tweet collected from the Streaming API.')
            # print(data)

            #handle twitterQuery2 collection
            twitterQuery2 = db1.twitterQuery2

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']
            # print out a message to the screen that we have collected a tweet
            print("Tweet created at: " + str(created_at))
            print('Converting Datetime to mongoDate..')
            # add field MongoDB datetime format
            dt = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
            datajson['mongoDate'] = dt

            # printing Date and Time of Tweet collection
            currentDT = datetime.datetime.now()
            print('Tweet collected at: ' + str(currentDT))

            # insert the data into the mongoDB into a collection called twitterQuery2
            # if twitter_search doesn't exist, it will be created.
            print('Inserting to MongoDB..')
            db1.twitterQuery2.insert(datajson)
            print('Inserted successfully.')
            print()
            print("next tweet:")
            return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
            return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


if __name__ == '__main__':
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')
    db1 = connection.twitter

    print("Database connection successful.")

    time.sleep(10)

    print("Crawler started after 10 seconds.")

    threats = ['#malware', '#apt', '#ransomware', '#spyware', '#xss', '#lfi', '#rfi', '#websecurity',
               '#xee', '#webappsec', '#botnet', '#DoS', '#DDoS', '#botmaster', '#botnets',
               '#phishing', '#phish', '#pharming', '#spam', '#idtheft', '#trojanvirus']

    # parser = get_parser()
    # args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key[0], config.consumer_secret[0])
    auth.set_access_token(config.access_token[0], config.access_secret[0])
    api = tweepy.API(auth)

    # twitter_stream = Stream(auth, MyListener(args.query))
    # twitter_stream.filter(track=[args.query])

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=threats)
