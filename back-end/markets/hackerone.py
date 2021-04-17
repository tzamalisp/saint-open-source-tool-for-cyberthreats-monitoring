import requests
from pprint import pprint
import json
from pymongo import MongoClient
import itertools
from datetime import datetime, date
import csv
from pprint import pprint
import numpy as np
from export_collection_data import zip_directory, datetime_limits_of_month

# crawling function of dynamic built website: JSON query to the database
def crawler(url, dateTimeStringCTI, timestampCTI, mongoDateCTI):

    mongoArrayCollection = []

    # iterate through site's pagination - queries to the website's server (starting at "1")
    for page in itertools.count(1):

        # adding the number of pagination page to the end of the url
        pg_url = '{}{}'.format(url, page)
        print(pg_url)
        print()

        # getting the right json file from each query
        try:
            resp = requests.get(pg_url).json()['results']
            if resp:
                # printing the type of the requested item that we get from the server
                print(type(resp))
                # adding the json documents to the main JSON objects collection
                mongoArrayCollection = mongoArrayCollection + resp
                # print(mongoArrayCollection)

                # printing the length of collection till now
                print(len(mongoArrayCollection))

                print()
                print('Next:')
        except ValueError as e:
            print('ValueError:', e)
            print('Finished! Crawler has not found any other pages on pagination')
            break

    # printing the length of collection after finishing whole pagination pages
    print('Length of documents list', len(mongoArrayCollection))
    print()
    print()
    print('Inserting documents to MongoDB:')

    # # drop collection if not empty
    # if dbMarkets.hackerone.count() != 0:
    #     dbMarkets.hackerone.drop()
    #     print('Database reset')
    # else:
    #     print('Database is empty! Starting storing data..')

    counter = 0

    # loop for adding each document of the JSON collection to the Database
    for item in mongoArrayCollection:
        # pprint(item)
        hackerone = dbMarkets.hackerone

        # Decode the JSON from hackerone
        jsonString = json.dumps(item)
        datajson = json.loads(jsonString)
        # adding datetime fields to each document
        datajson['DatetimeUTC-CTI'] = dateTimeStringCTI
        datajson['TimestampUTC-CTI'] = timestampCTI
        datajson['mongoDate-CTI'] = mongoDateCTI

        # pretty print of each document
        # pprint(datajson)

        # insert document to MongoDB
        dbMarkets.hackerone.insert(datajson)

        counter += 1

    print()
    print('Items inserted successfully to MongoDB!')
    # printing items added to MongoDB
    print('items counted:', counter)


def export_to_csv_json(csv_file, csv_columns):

    print('Starting converting to CSV:')
    print('Querying Database..')
    documents = dbMarkets.hackerone.find()

    counter = 0
    dictMongoList = []

    print('Scanning Database documents..')
    for document in documents:
        dictMongo = {}
        dictMongo['id'] = document.get('id')
        dictMongo['name'] = document.get('name')
        dictMongo['submission_state'] = document.get('meta').get('submission_state', 'null')
        dictMongo['bug_count'] = document.get('meta').get('bug_count', 'null')
        dictMongo['minimum_bounty'] = document.get('meta').get('minimum_bounty', 'null')
        dictMongo['default_currency'] = document.get('meta').get('default_currency', 'null')
        dictMongo['offers_bounties'] = document.get('meta').get('offers_bounties', 'null')
        dictMongo['DatetimeUTC-CTI'] = document.get('DatetimeUTC-CTI')
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



def export_hackerone_to_csv(csv_file, csv_columns, query):

    print('Starting converting to CSV:')
    print('Querying Database..')
    documents = dbMarkets.hackerone.find(query)

    counter = 0
    dictMongoList = []

    print('Scanning Database documents..')
    for document in documents:
        dictMongo = {}
        dictMongo['id'] = document.get('id')
        dictMongo['name'] = document.get('name')
        dictMongo['submission_state'] = document.get('meta').get('submission_state', 'null')
        dictMongo['bug_count'] = document.get('meta').get('bug_count', 'null')
        dictMongo['minimum_bounty'] = document.get('meta').get('minimum_bounty', 'null')
        dictMongo['default_currency'] = document.get('meta').get('default_currency', 'null')
        dictMongo['offers_bounties'] = document.get('meta').get('offers_bounties', 'null')
        dictMongo['DatetimeUTC-CTI'] = document.get('DatetimeUTC-CTI')
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


def export_hackerone_to_json(jsonExport):
    print('Starting converting to CSV:')
    print('Querying Database..')
    documents = dbMarkets.hackerone.find()

    counter = 0
    dictMongoList = []

    print('Scanning Database documents..')
    for document in documents:
        dictMongo = {}
        dictMongo['id'] = document.get('id')
        dictMongo['name'] = document.get('name')
        dictMongo['submission_state'] = document.get('meta').get('submission_state', 'null')
        dictMongo['bug_count'] = document.get('meta').get('bug_count', 'null')
        dictMongo['minimum_bounty'] = document.get('meta').get('minimum_bounty', 'null')
        dictMongo['default_currency'] = document.get('meta').get('default_currency', 'null')
        dictMongo['offers_bounties'] = document.get('meta').get('offers_bounties', 'null')
        dictMongo['DatetimeUTC-CTI'] = document.get('DatetimeUTC-CTI')
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


    # ---------------------------------------------------------------------------------------------------------------- #

def high_charts_timestamp(datetime_obj):
    """ This is a post processing function. It receives a pandas datetime element and takes care of producing
        a timestamp suitable for high charts library.
        @parameters
            datetime_obj                (datetime)
        @returns
            __high_charts_timestamp__   (timestamp)     readable by high charts library
    """

    # due to pandas processing the datetime_oj have always the structure xx:xx:xx 00:00:00 format
    # so retrieving year, month, day is all we need to begin converting

    datetime_obj_tuple = datetime_obj.timetuple()
    year = datetime_obj_tuple.tm_year
    month = datetime_obj_tuple.tm_mon
    day = datetime_obj_tuple.tm_mday
    # string
    high_charts_datetime_string = datetime(year, month, day, 14, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S.%f')
    # datetime
    high_charts_datetime_obj = datetime.strptime(high_charts_datetime_string, '%Y-%m-%d %H:%M:%S.%f')
    high_charts_timestamp = high_charts_datetime_obj.timestamp() * 1000

    return high_charts_timestamp

    # ---------------------------------------------------------------------------------------------------------------- #

def __high_charts_timestamp_to_date__(highcharts_timestamp):
    """ This is a post processing function. It receives a highcharts_timestamp and converts it back to date
        It is the reverse function of __high_charts_timestamp__.
            @parameters
                high_charts_timestamp   (timestamp)     readable by high charts library
            @returns
                                        (string)

        """
    dt = datetime.fromtimestamp(highcharts_timestamp/1000)

    return datetime(dt.year, dt.month, dt.day).strftime("%Y-%m-%d")

    # ---------------------------------------------------------------------------------------------------------------- #


def export_bounties_to_json(cursor, key, file_name, path):

    doc_list = []
    rate_list= []

    for doc in cursor.rewind():
        bug = doc.get('meta').get(key, 'null')
        datetime_obj =  doc.get('mongoDate-CTI')
        # If doc list has at least one element find the difference between two records
        if doc_list:
            rate_list.append([high_charts_timestamp(datetime_obj), bug-doc_list[-1][1]])
        doc_list.append([high_charts_timestamp(datetime_obj), bug])

    # files will be overwritten
    with open(path+file_name+".json", 'w') as json_file:
        json.dump(doc_list, json_file, separators=(',', ': '), indent=4)

    # added records json
    with open(path + file_name + "_rates.json", 'w') as json_file:
        json.dump(rate_list, json_file, separators=(',', ': '), indent=4)

    # ---------------------------------------------------------------------------------------------------------------- #

def export_bounties_to_csv(cursor, key, file_name, path):

    doc_list = []

    for doc in cursor.rewind():
        bug = doc.get('meta').get(key, 'null')
        datetime_obj = doc.get('mongoDate-CTI')
        doc_list.append([high_charts_timestamp(datetime_obj), bug])

    # files will be overwritten
    with open(path + file_name + ".csv", 'w') as csv_file:
        for result in doc_list:
            # highcharts timestamp must be converted in date before saved to csv. External use NCSR Demokritos
            date_notation = __high_charts_timestamp_to_date__(result[0])
            line = str(date_notation) + str(',') + str(result[1]) + str("\n")
            csv_file.write(line)

    # WARNING:no csv export option for rates
    # ---------------------------------------------------------------------------------------------------------------- #
"""function which calculates the sum of records in a daily frequency
    @input
        cursor  :   aggregation result cursor
        path    :   path of directory to store json records
    @Output
        stores a json file with name 'allBugsRatePerDay.json' under <path>
"""

def export_bountiesByDay_to_json(cursor, path):

    bounty_Day_list = []
    rate_list = []

    for doc in cursor:
        bugsNum = doc['counter']
        dtstr= doc['_id']['time']
        dt_obj = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
        bounty_Day_list.append([dt_obj, bugsNum])
    # sort list
    bounty_Day_list.sort(key=lambda x: x[0])
    recordCounter=0
    for record in bounty_Day_list:
        if recordCounter>0:
            diff=record[1]-bounty_Day_list[recordCounter-1][1]
            rate_list.append([high_charts_timestamp(record[0]),diff])
        recordCounter=recordCounter+1
    # files will be overwritten
    with open(path + "/allBugsRatePerDay.json", 'w') as json_file:
        json.dump(rate_list, json_file, separators=(',', ': '), indent=4)
    # ---------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':

    crawling_time = datetime.utcnow()
    print("Report on", crawling_time.strftime('%Y-%m-%d %H:%M:%S'), '\n')

    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')
    dbMarkets = connection.markets

    print("Database connection successful..")
    print()

    # getting timestamp in UTC in Microsecond accuracy
    print("Initial time in UTC:")
    ts = datetime.utcnow().timestamp()
    print(ts)
    valueDt = datetime.fromtimestamp(ts)
    dateTimeMongo = valueDt.strftime('%Y-%m-%d')
    print(valueDt)
    dateTimeMongoUTC = datetime.utcnow()

    # CTI datetime
    datetimeObjectUTCCTI = dateTimeMongoUTC
    print('Date MongoDB object:', datetimeObjectUTCCTI)
    datetimeUTCCTI = datetimeObjectUTCCTI.strftime('%Y-%m-%d')
    print('Date string format:', datetimeUTCCTI)

    # CTI timestamp
    timestampUTCCTI = ts

    print()

    # crawling function
    page = 'https://hackerone.com/directory?query=type%3Ahackerone&sort=resolved_reports_closed%3Adescending&page=1'
    indicator = 'https://hackerone.com/programs/search?query=type:hackerone&sort=published_at:descending&page='
    crawler(indicator, datetimeUTCCTI, timestampUTCCTI, datetimeObjectUTCCTI)

    # creating CSV file
    # csv_columns = ['id', 'name', 'submission_state', 'bug_count', 'minimum_bounty', 'default_currency',
    #                'offers_bounties', 'DatetimeUTC-CTI']
    # csv_file = '/var/www/html/saint/markets/dataset-bugBounties.csv'
    # json_file_export = '/var/www/html/saint/markets/dataset-bugBounties.json'

    # these function have been modified to export_hackerone_to_csv and export_hackerone_to_json
    # export_to_csv(csv_file, csv_columns)
    # export_to_json(json_file_export)

    # ---------------------------------------------------------------------------------------------------------------- #

    """ Export Datasets """
    # last datetime moment of this month must be based on crawling time to ensure synchronization
    start_of_month, end_of_month = datetime_limits_of_month(utcnow=crawling_time)

    csv_columns = ['id', 'name', 'submission_state', 'bug_count', 'minimum_bounty', 'default_currency',
                   'offers_bounties', 'DatetimeUTC-CTI']
    csv_file = '/var/www/html/saint/markets/dataset-bug-bounties/dataset-bug-bounties_{0}_{1}.csv'.format(crawling_time.year, crawling_time.month)
    json_file_export = '/var/www/html/saint/markets/dataset-bugBounties.json'

    print("\nRetrieving MongoDB's Collection...")
    try:
        query = {"mongoDate-CTI": {"$gte": start_of_month, "$lte": end_of_month}}
        results_cursor = dbMarkets.hackerone.find(query)
        export_hackerone_to_csv(csv_file, csv_columns, query)
    except Exception as e:
        print("__main__ > Export Datasets Phase: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    path = '/var/www/html/saint/markets/'
    export_path = '/var/www/html/saint/markets/dataset-bug-bounties/'
    zip_directory(export_path, "dataset-bug-bounties.zip", path)

    # ---------------------------------------------------------------------------------------------------------------- #

    """ Highcharts Exports """

    # BUG BOUNTIES - Highcharts and csv exports

    # change only this table in order to choose other Companies
    names = ["Yahoo!", "Shopify", "Uber", "Twitter", "Slack"]
    bug_count_path = path + "perday-bug-bounties-count/"

    for name in names:

        try:
            query = { "$and": [{"name":name}, {"meta.bug_count": {"$exists": 1}}, {"meta.bug_count": {"$ne": None}}, {"mongoDate-CTI":{"$ne": None}}] }
            projection = {"_id": 0, "mongoDate-CTI": 1, "meta.bug_count":1}
            cursor = dbMarkets.hackerone.find(query, projection)

            # no file extension for file name
            file_name = "perday-bug-bounties-count-{0}".format(name)
            export_bounties_to_json(cursor, "bug_count", file_name, path)
            export_bounties_to_csv(cursor, "bug_count", file_name, bug_count_path)

        except Exception as e:
            print("__main__ > Export Datasets Phase: ", e)
            # destroy cursor, it won't be used again
            cursor = None

    zip_directory(bug_count_path, "perday-bug-bounties-count.zip", path)

    # BUG BOUNTIES - Means
    bug_count_means_list = []

    for name in names:

        bug_count_cursor = dbMarkets.hackerone.aggregate([
            {"$match": {"name": name}},
            {"$group": {
                "_id": {"name": "$name", "DatetimeUTC-CTI": "$DatetimeUTC-CTI",
                        "bug_count": {"$max": "$meta.bug_count"}}}}
        ]
        )

        bug_count_list = []
        # pprint(len(list(results_cursor)))
        for doc in bug_count_cursor:
            bug_count_list.append(doc.get("_id").get("bug_count"))

        mean = np.mean(bug_count_list)
        mean = mean.round(0)

        bug_count_means_list.append([name, mean])

    print(bug_count_means_list)
    with open(path + "bug-bounty-count-means.json", 'w') as json_file:
        json.dump(bug_count_means_list, json_file, separators=(',', ': '), indent=4)

    with open(path + "bug-bounty-count-means.csv", 'w') as csv_file:
        for entity in bug_count_means_list:
            csv_file.write(str(entity[0]) + str(',') + str(entity[1]) + str("\n"))

    # ---------------------------------------------------------------------------------------------------------------- #

    # MINIMUM BOUNTIES - Highcharts and csv exports
    minimum_bug_path = path + "perday-bug-bounties-minimum/"
    minimum_bounty = []

    for company_name in names:

        try:
            query = { "$and": [{"name":company_name}, {"meta.minimum_bounty": {"$exists": 1}}, {"meta.minimum_bounty": {"$ne": None}}, {"mongoDate-CTI":{"$ne": None}}] }
            projection = {"_id": 0, "mongoDate-CTI": 1, "meta.minimum_bounty":1}
            results_cursor = dbMarkets.hackerone.find(query, projection)

            # no file extension for file name
            file_name = "perday-bug-bounties-minimum-{0}".format(company_name)
            export_bounties_to_json(results_cursor, "minimum_bounty", file_name, path)
            export_bounties_to_csv(results_cursor, "minimum_bounty", file_name, minimum_bug_path)

        except Exception as e:
            print("__main__ > Export Datasets Phase: ", e)
            # destroy cursor, it won't be used again
            results_cursor = None

    zip_directory(minimum_bug_path, "perday-bug-bounties-minimum.zip", path)


    # MINIMUM BOUNTIES - Means

    minimum_bounty_means_list = []

    for name in names:

        minimum_bounties_cursor = dbMarkets.hackerone.aggregate([
            {"$match": {"name": name}},
            {"$group": {
                "_id": {"name": "$name", "DatetimeUTC-CTI": "$DatetimeUTC-CTI",
                        "minimum_bounty": {"$max": "$meta.minimum_bounty"}}}}
        ]
        )

        minimum_bounty_list = []
        for doc in minimum_bounties_cursor:
            minimum_bounty_list.append(doc.get("_id").get("minimum_bounty"))

        mean = np.mean(minimum_bounty_list)
        mean = mean.round(0)

        minimum_bounty_means_list.append([name, mean])

    print(minimum_bounty_means_list)
    with open(path + "bug-bounty-minimum-bounties-means.json", 'w') as json_file:
        json.dump(minimum_bounty_means_list, json_file, separators=(',', ': '), indent=4)

    with open(path + "bug-bounty-minimum-bounties-means.csv", 'w') as csv_file:
        for entity in minimum_bounty_means_list:
            csv_file.write(str(entity[0]) + str(',') + str(entity[1]) + str("\n"))
# ---------------------------------------------------------------------------------------------------------------- #

# Bugs added per day - aggregation and Highchart json export
    print('Get sum of bugs for every day(aggregation)')
    try:
        queryEveryDaySum = [{'$project': {'_id': 0, 'mongoDate-CTI': 1, 'meta.bug_count': 1}},
                  {'$group': {'_id': {
                      'day': {'$dayOfYear': '$mongoDate-CTI'},
                      'year': {'$year': '$mongoDate-CTI'},
                      'time': {'$dateToString': {
                              'format': '%Y-%m-%d %H:%M:%S',
                              'date': '$mongoDate-CTI'}}},
                    'counter': {'$sum': '$meta.bug_count'}}}]
        cursorEveryDaySum = dbMarkets.hackerone.aggregate(queryEveryDaySum)
    except Exception as e:
        print("Unexpected error:", type(e), e)


    export_bountiesByDay_to_json(cursorEveryDaySum,path)
