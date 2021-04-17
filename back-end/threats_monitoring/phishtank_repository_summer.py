from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from descriptive_analysis import DescriptiveAnalysis
from export_collection_data import ExportCollectionData
from today_limits import today_datetime


def connect_to_mongodb():
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    return db

# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":

    print("Report on", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '\n')

    """ Set Path Of Data Exportation """
    # to run on server
    server_path = '/var/www/html/saint/indicators2018/phishing/'
    # to run locally
    local_path = ""

    db = connect_to_mongodb()

    """ Today's Phishing Attacks """
    today_start, today_end = today_datetime()
    cursor = db.threats.phishtank.find({"mongoDate": {"$gte": today_start, "$lt": today_end}})

    docs_match_update, docs_modified_update, docs_inserted  = 0, 0, 0
    for doc in cursor:
        try:
            upd_res = db.threats.phishtank_repository.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert = True)
            docs_match_update += upd_res.matched_count
            docs_modified_update += upd_res.modified_count
            if upd_res.upserted_id is not None:
                docs_inserted += 1
        except OperationFailure as e:
            print("Error in mongoDB operation > ", e)

    print("Documents Inserted: ", docs_inserted)
    print("Documents Matched Update Filter: ", docs_match_update)
    print("Documents Modified: ", docs_modified_update)

    """ Descriptive Analysis for Phishing Repository"""
    analysis = DescriptiveAnalysis(collection=db.threats.phishtank_repository, path=server_path)
    analysis(query={}, projection={"_id": 0})
    # Time Series Anaalysis
    data_frame = analysis.time_series_analysis('mongoDate')
    analysis.data_frame_to_csv(data_frame, "perdayTimeSeriesPhishing")
    analysis.data_frame_to_json(data_frame, "perdayTimeSeriesPhishing")
    # Top Author Categorical Analysis
    last_week = datetime.utcnow() - timedelta(days=7)
    analysis_2 = DescriptiveAnalysis(collection=db.threats.phishtank_repository, path=server_path)
    analysis_2(query={'mongoDate': {"$gte": last_week}}, projection={"_id": 0})
    top5 = analysis_2.top_n(5, "Submitted-by", "phishing-top-submitters")
    print(top5)

    ''' Export Current MongoDB Collection Instance '''
    # exploitDataBase = ExportCollectionData(collection=db.threats.phishtank_repository, path=server_path)
    # exploitDataBase(query={}, projection={"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0})
    # exploitDataBase.export_collection_to_json("dataset-phishing")
    # csv_header = ["URL", "Submitted-by", "Valid", "Online", "DatetimeUTC", "TimestampUTC",
    #                       "DatetimeUTC-CTI", "TimestampUTC-CTI", "Entity-type", "Category"]
    # exploitDataBase.export_collection_to_csv("dataset-phishing", csv_header)