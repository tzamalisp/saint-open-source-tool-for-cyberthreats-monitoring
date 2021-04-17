
# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python3 twitterCrawlerV3.py -q google -d data
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

# connect to database
connection = MongoClient('127.0.0.1', 27017)


#connect to database "twitter"
db = connection.admin
db.authenticate('supersaint', 'eurosnt2017')

db1 = connection.googles

print("connection successful")

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                print(data)

                #handle to googles collection
                output1 = db1.output1

                # Decode the JSON from Twitter
                datajson = json.loads(data)

                # #grab the 'created_at' data from the Tweet to use for display
                created_at = datajson['created_at']
                # add field MongoDB datetime format
                dt = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
                datajson['mongoDate'] = dt

                #insert the data into the mongoDB into a collection called googles
                #if twitter_search doesn't exist, it will be created.
                db1.output1.insert(datajson)


                #print out a message to the screen that we have collected a tweet
                print("Tweet collected at " + str(created_at))
                currentDT = datetime.datetime.now()
                print (str(currentDT))
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
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key[2], config.consumer_secret[2])
    auth.set_access_token(config.access_token[2], config.access_secret[2])
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
twitter_stream.filter(track=[args.query])