import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
import pprint
import pymongo
import json
from pymongo import MongoClient
import csv
import string

import datetime

# connect to database
connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
db = connection.admin
db.authenticate('xxxxxx', 'xxxXXXxxxXX')
dbThreats = connection.threats

print("Database connection successful..")
print()

# getting timestamp in UTC in Microsecond accuracy
print("Time in UTC:")
ts = datetime.datetime.utcnow().timestamp()
print(ts)
valueDt = datetime.datetime.fromtimestamp(ts)
dateTimeMongo = valueDt.strftime('%Y-%m-%d %H:%M:%S')
print(valueDt)
dateTimeMongoUTC = datetime.datetime.utcnow()

# CTI datetime
datetimeObjectUTCCTI = dateTimeMongoUTC
datetimeUTCCTI = datetimeObjectUTCCTI.strftime('%Y-%m-%d %H:%M:%S')

# CTI timestamp
timestampUTCCTI = ts

print()

# drop collection if not empty
if dbThreats.webBasedAttacks2.count() != 0:
    dbThreats.webBasedAttacks2.drop()
    print('Database reset')
else:
    print('Database is empty! Starting retrieving data..')

# indicator link
indicator = 'http://feeds.dshield.org/block.txt'



def download(url):
    print('Downloading site..')

    try:
        with urllib.request.urlopen(url) as response:
            htmlPage = response.readlines()

            linesPage = []

            for line in htmlPage:
                linesPage.append(line)

            countingPage = linesPage[28:]

            # print(countingPage)

            header = str(countingPage[0].decode('ascii'))
            print(header)
            header = header.rstrip("\n")
            headerList = header.split("\t")

            print(headerList)

            print()
            print('Values:')

            dictlistMongo = []

            for row in countingPage[1:]:
                rowNew = str(row.decode('ascii'))
                rowNew = rowNew.rstrip("\n")
                rowNew = rowNew.rstrip(",")
                rowList = rowNew.split("\t")
                dictlistMongo.append(dict(zip(headerList, rowList)))

            for dictionary in dictlistMongo:
                dictionary['Name'] = dictionary['Name'].rstrip(",")
                dictionary['Name'] = dictionary['Name'].rstrip(" ")
                dictionary['Netmask'] = int(dictionary['Netmask'])
                dictionary['Attacks'] = int(dictionary['Attacks'])
                dictionary['Entity type'] = 'IP'
                dictionary['Category'] = 'Web Based Attacks'
                dictionary['TimestampUTC'] = ts
                dictionary['DatetimeUTC'] = dateTimeMongo

            # pprint.pprint(dictlistMongo)

            for dictionaryMongo in dictlistMongo:
                print(dictionaryMongo)
                # handle to web based attacks (1) collection
                webBasedAttacks2 = dbThreats.webBasedAttacks2

                # Decode the JSON from Twitter
                jsonString = json.dumps(dictionaryMongo)
                datajson = json.loads(jsonString)

                # insert the data into the mongoDB into a collection called webBased
                # if twitter_search doesn't exist, it will be created.
                dbThreats.webBasedAttacks2.insert(datajson)

            print()
            print("Data inserted successfully to Database")

    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Error downloading page:', e.reason)


def fetchDataFromDB():
    # find the right collection
    webBasedAttacks2 = dbThreats.webBasedAttacks2



    if webBasedAttacks2.count() != 0:

        # db.webBasedAttacks2.find({}, {'Name': 1, 'Country': 1, 'Attacks': 1, '_id': 0})

        query = {}
        # query = {'title': {'$regex': 'apple|google', '$options': 'i'}}
        projection = {'Name': 1, 'Country': 1, 'Attacks': 1, '_id': 0}
        # projection = {'title': 1, '_id': 0}
        try:
            cursor = webBasedAttacks2.find(query, projection)
            # cursor = cursor.limit(10)

        except Exception as e:
            print("Unexpected error:", type(e), e)

        with open('/var/www/html/saint/indicators2018/web-based-attacks/top20WebBasedAttacks.csv', 'w') as f:
            for doc in cursor:
                name = doc['Name'][0:56]
                name2 = name.replace(',', '')
                country = doc['Country']
                attacks = doc['Attacks']
                print(name2)
                data = name2 + ' ' + '(' + country + ')' + ',' + str(attacks)
                # print(data)
                f.write(data)
                f.write('\n')

        print()
        print("Writing to CSV --> complete!")


# ----------------------------------------------------------------------------------------------------


def csvToJson():

    jsonBarPlotsWebBasedAttacks = []
    with open('/var/www/html/saint/indicators2018/web-based-attacks/top20WebBasedAttacks.csv') as csvfileWebBasedAttacks:
        readCSVWebBasedAttacks = csv.reader(csvfileWebBasedAttacks, delimiter=',')
        next(readCSVWebBasedAttacks)
        for row in readCSVWebBasedAttacks:
            row[1] = int(row[1])
            jsonBarPlotsWebBasedAttacks.append(row)

    print()
    print('new file Web Based Attacks (2) Bar Plots:')
    print(jsonBarPlotsWebBasedAttacks)

    print()
    print('Writing..')
    with open('/var/www/html/saint/indicators2018/web-based-attacks/top20WebBasedAttacks.json', 'w') as file:
        json.dump(jsonBarPlotsWebBasedAttacks, file, indent=4)

    print('Writing Top 20 Web Based Attacks JSON complete!')

if __name__ == '__main__':

    download(indicator)

    fetchDataFromDB()

    csvToJson()

