import requests
from pprint import pprint
import json
from pymongo import MongoClient
import itertools
from datetime import datetime
import csv


def export_to_csv(csv_file, csv_columns):

    print('Starting converting to CSV:')
    print('Querying Database..')
    documents = dbMarkets.zerodium.find()

    counter = 0
    dictMongoList = []

    print('Scanning Database documents..')
    for document in documents:
        dictMongo = {}
        dictMongo['Device-Type'] = document.get('Device-Type')
        dictMongo['Operating-System'] = document.get('Operating-System')
        dictMongo['Issue'] = document.get('Issue')
        dictMongo['Type'] = document.get('Type')
        dictMongo['Price'] = document.get('Price')
        dateObject = document.get('Date')
        # print(dateObject)

        dateString = dateObject.strftime('%Y-%m-%d')
        # print(dateString)
        dictMongo['Date'] = dateString
        dictMongoList.append(dictMongo)

        # pprint(dictMongo)
        # print()
        # print('Next document:')
        counter += 1

    print('Number of documents scanned:', counter)
    print('Length of List with dictionaries:', len(dictMongoList))

    print('Writing CSV file..')

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dictMongoList:
                writer.writerow(data)
    except ValueError as e:
        print('Error:', e)

    print('Writing Complete!')


def export_to_json(jsonExport):
    print('Starting converting to CSV:')
    print('Querying Database..')
    documents = dbMarkets.zerodium.find()

    counter = 0
    dictMongoList = []

    print('Scanning Database documents..')
    for document in documents:
        dictMongo = {}
        dictMongo['Device-Type'] = document.get('Device-Type')
        dictMongo['Operating-System'] = document.get('Operating-System')
        dictMongo['Issue'] = document.get('Issue')
        dictMongo['Type'] = document.get('Type')
        dictMongo['Price'] = document.get('Price')
        dateObject = document.get('Date')

        dateString = dateObject.strftime('%Y-%m-%d')
        # print(dateString)
        dictMongo['Date'] = dateString
        dictMongoList.append(dictMongo)

        # pprint(dictMongo)
        # print()
        # print('Next document:')
        counter += 1

    print('Number of documents scanned:', counter)
    print('Length of List with dictionaries:', len(dictMongoList))

    print('Writing JSON file..')

    dictMongoListJsonReady = json.dumps(dictMongoList, indent=4)
    f = open(jsonExport, "w")
    f.write(dictMongoListJsonReady)
    f.close()

    print('Writing Complete!')


if __name__ == '__main__':
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')
    dbMarkets = connection.markets

    print("Database connection successful..")
    print()

    # creating CSV file
    csv_columns = ['Device-Type', 'Operating-System', 'Issue', 'Type', 'Price', 'Date']
    csv_file = '/var/www/html/saint/markets/dataset-market-exploits.csv'
    json_file_export = '/var/www/html/saint/markets/dataset-market-exploits.json'

    export_to_csv(csv_file, csv_columns)
    export_to_json(json_file_export)
