import requests
from pprint import pprint
import json
from pymongo import MongoClient
import itertools
from datetime import datetime, date, time, timedelta
import csv
from pprint import pprint
import numpy as np
from export_collection_data import zip_directory, datetime_limits_of_month

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
def export_bountiesByDay_to_json(cursor, path):

    bounty_Day_list = []
    rate_list = []
    rate_list_percent = []

    for doc in cursor:
        #print('Date: %s bugs: %d' % (doc['_id']['time'], doc['counter']))
        bugsNum = doc['counter']
        dtstr= doc['_id']['time']
        dt_obj = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
        #bounty_Day_list.append([high_charts_timestamp(dt_obj), bugsNum])
        bounty_Day_list.append([dt_obj, bugsNum])
    # sort list
    bounty_Day_list.sort(key=lambda x: x[0])
    recordCounter=0
    for record in bounty_Day_list:
        if recordCounter>0:
            #print(record[1]-bounty_Day_list[recordCounter-1][1])
            diff=record[1]-bounty_Day_list[recordCounter-1][1]
            diff_percent = ((diff*100)/bounty_Day_list[recordCounter-1][1])
            rate_list.append([high_charts_timestamp(record[0]),diff])
            rate_list_percent.append([high_charts_timestamp(record[0]),100*diff_percent])

        # else:
        #     rate_list.append([high_charts_timestamp(record[0]-timedelta(days=1)),1])
        recordCounter=recordCounter+1
    # files will be overwritten
    with open(path + "/allBugsRatePerDay.json", 'w') as json_file:
        json.dump(rate_list, json_file, separators=(',', ': '), indent=4)
    #
    for record in bounty_Day_list:
        record[0]=high_charts_timestamp(record[0])
    with open(path + "/allBugsPerDay.json", 'w') as json_file:
        json.dump(bounty_Day_list, json_file, separators=(',', ': '), indent=4)
    with open(path + "/allBugs_percent_PerDay.json", 'w') as json_file:
        json.dump(rate_list_percent, json_file, separators=(',', ': '), indent=4)


    # ---------------------------------------------------------------------------------------------------------------- #


def export_bounties_to_json(cursor, key, file_name, path):

    doc_list = []

    for doc in cursor.rewind():
        bug = doc.get('meta').get(key, 'null')
        datetime_obj =  doc.get('mongoDate-CTI')
        doc_list.append([high_charts_timestamp(datetime_obj), bug])

    # files will be overwritten
    with open(path+file_name+".json", 'w') as json_file:
        json.dump(doc_list, json_file, separators=(',', ': '), indent=4)


    # ---------------------------------------------------------------------------------------------------------------- #
def export_bounties_and_rates_to_json(cursor, key, file_name, path):

    doc_list = []
    rate_list= []
    rate_list_percent = []

    for doc in cursor.rewind():
        bug = doc.get('meta').get(key, 'null')
        datetime_obj =  doc.get('mongoDate-CTI')
        if doc_list:
            rate_list.append([high_charts_timestamp(datetime_obj), bug-doc_list[-1][1]])
            rate_list_percent.append([high_charts_timestamp(datetime_obj), ((bug - doc_list[-1][1])*100/doc_list[-1][1])])
        doc_list.append([high_charts_timestamp(datetime_obj), bug])

    # files will be overwritten
    with open(path+file_name+".json", 'w') as json_file:
        json.dump(doc_list, json_file, separators=(',', ': '), indent=4)

    # files will be overwritten
    with open(path + file_name + "_rates.json", 'w') as json_file:
        json.dump(rate_list, json_file, separators=(',', ': '), indent=4)

    # rate list percent json
    with open(path + file_name + "_rates_percent.json", 'w') as json_file:
        json.dump(rate_list_percent, json_file, separators=(',', ': '), indent=4)
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

    # ---------------------------------------------------------------------------------------------------------------- #

def export_bounties_and_rates_to_csv(cursor, key, file_name, path):

    doc_list = []
    rate_list = []
    rate_list_percent = []

    for doc in cursor.rewind():
        bug = doc.get('meta').get(key, 'null')
        datetime_obj = doc.get('mongoDate-CTI')
        if doc_list:
            rate_list.append([high_charts_timestamp(datetime_obj), bug - doc_list[-1][1]])
            rate_list_percent.append([high_charts_timestamp(datetime_obj), ((bug - doc_list[-1][1])*100/doc_list[-1][1])])
        doc_list.append([high_charts_timestamp(datetime_obj), bug])

    # files will be overwritten
    with open(path + file_name + ".csv", 'w') as csv_file:
        for result in doc_list:
            # highcharts timestamp must be converted in date before saved to csv. External use NCSR Demokritos
            date_notation = __high_charts_timestamp_to_date__(result[0])
            line = str(date_notation) + str(',') + str(result[1]) + str("\n")
            csv_file.write(line)

    with open(path + file_name + "_rates.csv", 'w') as csv_file:
        for result in rate_list:
            # highcharts timestamp must be converted in date before saved to csv. External use NCSR Demokritos
            date_notation = __high_charts_timestamp_to_date__(result[0])
            line = str(date_notation) + str(',') + str(result[1]) + str("\n")
            csv_file.write(line)

    # write files with percentage change

    with open(path + file_name + "_rates_percent.csv", 'w') as csv_file:
        for result in rate_list_percent:
            # highcharts timestamp must be converted in date before saved to csv. External use NCSR Demokritos
            date_notation = __high_charts_timestamp_to_date__(result[0])
            line = str(date_notation) + str(',') + str(result[1]) + str("\n")
            csv_file.write(line)

    # ---------------------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    timeNow = datetime.utcnow()
    print("Report on", timeNow.strftime('%Y-%m-%d %H:%M:%S'), '\n')

    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')
    dbMarkets = connection.markets

    print("Database connection successful..")
    print()

    # midnightToday = datetime.combine(datetime.today(), time.min)
    # midnightYesterday = midnightToday - timedelta(days=1)
    # midnight2DaysAgo = midnightToday - timedelta(days=2)
    # midnightTomorrow = midnightToday + timedelta(days=1)
    # print('Midnight today:', midnightToday)
    # print('Midnight yesterday:', midnightYesterday)
    # print('Midnight 2 days ago:', midnight2DaysAgo)
    # print('Midnight tomorrow:', midnightTomorrow)
    #
    # print()
    # print('Starting today querying the database:')
    #
    # # query
    # try:
    #     queryToday = [{'$match': {'mongoDate-CTI': {'$gte': midnightToday, '$lt': midnightTomorrow}}},
    #                   {'$project': {'_id': 0, 'mongoDate-CTI': 1, 'meta.bug_count': 1}},
    #                   {'$group': {'_id': 'result', 'counter': {'$sum': '$meta.bug_count'}}}]
    #
    #     cursorToday = dbMarkets.hackerone.aggregate(queryToday)
    # except Exception as e:
    #     print("Unexpected error:", type(e), e)
    #
    # print()
    # print('RESULTS:')
    # print()
    # bugsToday = 0
    # for doc in cursorToday:
    #     print('Bug counts today:', doc)
    #     bugsToday = doc['counter']
    #
    # print()
    # print()
    # print('Starting yesterday querying the database:')
    #
    # # query
    # try:
    #     queryYesterday = [{'$match': {'mongoDate-CTI': {'$gte': midnightYesterday, '$lt': midnightToday}}},
    #               {'$project': {'_id': 0, 'mongoDate-CTI': 1, 'meta.bug_count': 1}},
    #               {'$group': {'_id': 'result', 'counter': {'$sum': '$meta.bug_count'}}}]
    #     cursorYesterday = dbMarkets.hackerone.aggregate(queryYesterday)
    # except Exception as e:
    #     print("Unexpected error:", type(e), e)
    #
    # print()
    # print('RESULTS:')
    # print()
    # bugsYesterday = 0
    # for doc in cursorYesterday:
    #     print('Bug counts yesterday:', doc)
    #     bugsYesterday = doc['counter']
    #
    # print('Bugs Today - Bugs Yesterday =', bugsToday - bugsYesterday)

    # change only this table in order to choose other Companies
    names = ["Yahoo!", "Shopify", "Uber", "Twitter", "Slack"]
    #names = ["Coinbase"]
    path = '/var/www/html/saint/markets/'
    export_path = '/var/www/html/saint/markets/dataset-bug-bounties/'
    #bug_count_path = path + "perday-bug-bounties-count/"
    bug_count_path = path

    for name in names:

        try:
            query = { "$and": [{"name":name}, {"meta.bug_count": {"$exists": 1}}, {"meta.bug_count": {"$ne": None}}, {"mongoDate-CTI":{"$ne": None}}] }
            projection = {"_id": 0, "mongoDate-CTI": 1, "meta.bug_count":1}
            cursor = dbMarkets.hackerone.find(query, projection)

            file_name = "perday-bug-bounties-count-{0}".format(name)
            export_bounties_to_json(cursor, "bug_count", file_name, path)

            # no file extension for file name
            #file_name = "perday-bug-bounties-count-{0}".format(name)
            export_bounties_and_rates_to_json(cursor, "bug_count", file_name, path)
            export_bounties_and_rates_to_csv(cursor, "bug_count", file_name, bug_count_path)
            for doc in cursor.rewind():
                bug = doc.get('meta').get("bug_count", 'null')
                datetime_obj = doc.get('mongoDate-CTI')
                #print("datetime: %s val: %d" % (datetime_obj.strftime('%Y-%m-%d'),bug))

        except Exception as e:
            print("__main__ > Export Datasets Phase: ", e)
            # destroy cursor, it won't be used again
            cursor = None

    # query for every day count
    print('Get sum of bugs for every day:')
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

    print()
    print('RESULTS:')
    print()
    #bugsYesterday = 0
    # for doc in cursorEveryDaySum:
    #     print('Date: %s bugs: %d' % (doc['_id']['time'],doc['counter']))
    export_bountiesByDay_to_json(cursorEveryDaySum,path)
    #zip_directory(bug_count_path, "perday-bug-bounties-count.zip", path)
