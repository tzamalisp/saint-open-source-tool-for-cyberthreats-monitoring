from datetime import timedelta
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from descriptive_analysis import *
from export_collection_data import *


def connect_to_mongodb():
    """ This function implements the connection to the mongoDb
        @returns
            connection  (MongoClient)   a MongoClient object to handle the connection
    """

    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    return db

# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":

    crawling_time = datetime.utcnow()
    print("Report on", crawling_time.strftime('%Y-%m-%d %H:%M:%S'), '\n')

    print("\nConnecting to MongoDB Data Base")
    db = connect_to_mongodb()

    """ Retrieve Today's Phishing Attacks from Current Instance and record them in Repository """
    print("Collecting today's attack from MongoDB's phishtank collection")
    today_start, today_end = today_datetime(crawling_time)
    cursor = db.threats.phishtank.find({"mongoDate": {"$gte": today_start, "$lt": today_end}})

    print("Storing Data...", end=' ')
    docs_match_update, docs_modified_update, docs_inserted = 0, 0, 0
    for doc in cursor:
        try:
            upd_res = db.threats.phishtank_repository.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
            docs_match_update += upd_res.matched_count
            docs_modified_update += upd_res.modified_count
            if upd_res.upserted_id is not None:
                docs_inserted += 1
        except OperationFailure as e:
            print("Error in mongoDB operation > ", e)

    print("Completed")
    print("Documents Inserted: ", docs_inserted)
    print("Documents Matched Update Filter: ", docs_match_update)
    print("Documents Modified: ", docs_modified_update)
    # -----------------------------------------------------------------------------------------------------------------#

    """ Descriptive Analysis """
    # set path of produced files
    path = '/var/www/html/saint/indicators2018/phishing/'

    # Time Series Section
    from pathlib import Path
    time_series_file = Path(path + 'perdayTimeSeriesPhishing.json')

    # set the appropriate query
    if time_series_file.exists():
        # retrieve ONLY today's data
        today_start, today_end = today_datetime(crawling_time)
        query = {"mongoDate": {"$gte": today_start, "$lte": today_end}}
        print('\nFile perdayTimeSeriesPhishing.json exists. Retrieve today attacks')
    else:
        # there is no analysis file, so retrieve the entire collection and create one
        query = {}
        print('\nFile perdayTimeSeriesPhishing.json does not exist. Retrieve the entire collection')
    # set the projection
    projection = {"_id": 0, "mongoDate": 1}

    try:
        results_cursor = db.threats.phishtank_repository.find(query, projection)
        attack_data_frames = time_series_analysis(results_cursor, mongo_date_type='mongoDate')
        # updates both csv and json files. Specify name with NO EXTENSION
        update_time_series_analysis_files(attack_data_frames, "perdayTimeSeriesPhishing", path)
    except Exception as e:
        print("__main__ > Descriptive Analysis Phase > Time Series Section: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    # Barplot Section / Top Submitters Categorical Analysis
    last_week = datetime.utcnow() - timedelta(days=7)
    query = {"mongoDate": {"$gte": last_week}}
    projection = {"_id": 0}

    try:
        last_week_results_cursor = db.threats.phishtank_repository.find(query, projection)
        # find last weeks top 10 countries and save them to csv and json. Specify name with NO EXTENSION
        top_submitters = top_n(last_week_results_cursor, 5, 'Submitted-by', 'phishing-top-submitters', path)
        print("\nLast Week's Top 5 Phish Submitters\n", top_submitters)
    except Exception as e:
        print("__main__ > descriptive analysis phase > Barplot Analysis: ", e)
        # destroy cursor, it won't be used again
        last_week_results_cursor = None
    # -----------------------------------------------------------------------------------------------------------------#

    """ Export Datasets """
    # last datetime moment of this month must be based on crawling time to ensure synchronization
    start_of_month, end_of_month = datetime_limits_of_month(utcnow=crawling_time)

    # If you want to produce a dataset of a past month just uncomment below and modify the example
    # and change dataset name too!
    # start_of_month, end_of_month = datetime_limits_of_month(utcnow=None, set_year=2018, set_month=8)

    export_path = path + 'dataset-phishing/'
    phishtank_repository_csv_header = ["URL", "Submitted-by", "Valid", "Online", "DatetimeUTC", "TimestampUTC",
                            "DatetimeUTC-CTI", "TimestampUTC-CTI", "Entity-type", "Category"]
    dataset_name = 'dataset_phishing_{0}_{1}.csv'.format(crawling_time.year, crawling_time.month)

    print("\nRetrieving MongoDB's Collection...")
    try:
        query = {"mongoDate": {"$gte": start_of_month, "$lte": end_of_month}}
        projection = {"_id": 0, "mongoDate":0, "mongoDate-CTI": 0}
        results_cursor = db.threats.phishtank_repository.find(query, projection)
        export_to_csv(results_cursor, dataset_name, phishtank_repository_csv_header, export_path)
    except Exception as e:
        print("__main__ > Export Datasets Phase: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None

    zip_directory(export_path, "dataset-phishing.zip", path)


