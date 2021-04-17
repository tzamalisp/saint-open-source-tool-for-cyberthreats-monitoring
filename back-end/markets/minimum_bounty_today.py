import requests
from pprint import pprint
import json
from pymongo import MongoClient
import itertools
from datetime import datetime
import csv


def find_todays_bounties():
    # Get today.
    from datetime import date
    from datetime import datetime
    dt = date.today()
    startday = datetime.combine(dt, datetime.min.time())
    print(startday)

    print('Querying Database..')
    documents = dbMarkets.hackerone.find({'$and': [{'$or': [{'name': 'Slack'}, {'name': 'Twitter'}, {'name': 'Uber'},
                                                            {'name': 'Shopify'}, {'name': 'Yahoo!'}]},
                                                   {'mongoDate-CTI': {'$gte': startday}}]},
                                         {'_id': 0, 'name': 1, 'meta.minimum_bounty': 1})


    dictMinimumBountyToday = []

    for doc in documents:
        dictEachDoc = []
        dictEachDoc.append(doc['name'])
        dictEachDoc.append(doc['meta']['minimum_bounty'])
        dictMinimumBountyToday.append(dictEachDoc)


    print(dictMinimumBountyToday)

    print('Writing JSON file..')
    with open('/var/www/html/saint/markets/minimum_bounties_perday.json', 'w') as file:
        json.dump(dictMinimumBountyToday, file, indent=4)
    print('Writing Minimum Bounties for Today JSON file completed!')


if __name__ == '__main__':
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')
    dbMarkets = connection.markets

    print("Database connection successful..")
    print()

    find_todays_bounties()
