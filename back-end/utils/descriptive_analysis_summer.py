from collections import Counter
import pandas as pd
from datetime import datetime
import json


class DescriptiveAnalysis:

    def __init__(self, collection, path):
        """ Prepares the class instance by specifying the collection to retrieve data from and the path to create files
        @param
            collection:         (MongoClient)       the full namespace of a collection eg. db.threats.WebBasedAttacks
            path:               (string)            the path to create and store data files
        """

        self.__collection = collection
        self.__path = path
        self.__query_results = []

    # -----------------------------------------------------------------------------------------------------------------#


    def __call__(self, query=None, projection=None):
        """ __call__ function is all about do the query of desire and take back the results.
            The cursor returned by the result is iterated once and all result documents are stored in the class variable
            query_results. This way data can be accessed many times without applying the same query multiple times
            or rewinding the cursor again and again (that may lead to unpleasant results). Also passing query_data as
            parameter between functions is avoided as long as it's class variable, accessible within class anytime
            @param
                query       (dictionary)    the query-filter to be applied. Default is no filter {}
                projection
            @returns
                documents_retrieved
                        (integer or None)   a count of docs stored in json
        """

        # Default parameters are mutable.
        # Default parameters are created only once. All future calls may be affected by first call
        if query is None:
            query = {}
        if projection is None:
            projection = {"_id": 0}

        try:
            cursor = self.__collection.find(query, projection)
            for doc in cursor:
                self.__query_results.append(doc)
            documents_retrieved = len(self.__query_results)
        except Exception as e:
            print("DescriptiveAnalysis > __call__ : Query MongoDB Error: ", e)
            documents_retrieved = None

        return documents_retrieved

    # -----------------------------------------------------------------------------------------------------------------#


    def time_series_analysis(self, mongoDateType='mongoDate', entity_type=''):
        """ Collects all the information from the collection and presents the number of blocked IP's per day
            Saves the results in csv and json file respectively for later process (stakeholders and Highcharts)
            @param
                db:     (Mongo Client)  this is the connection returned by Pymongo Client,
                                        we take it from connect_to_mongodb() function
        """

        num_of_docs_in_collection = self.__collection.count()

        # process data if the collection only if it's not empty
        # if it empty return no analysis can be done
        if num_of_docs_in_collection == 0:
            try:
                raise Warning("No documents retrieved. Collection {} seems to be empty".format(self.__collection.name))
            except Exception as e:
                print("DescriptiveAnalysis > time_series_analysis: ", e)
            return None

        if entity_type in ['IP', 'URL', 'Domain']:
            docs_of_interest = list([])
            for doc in self.__query_results:
                if doc["Entity-Type"] == entity_type:
                    docs_of_interest.append(doc)
        # in any other case entity-type is considered as an empty string by default
        # so the whole collection is retrieved
        else:
            docs_of_interest = self.__query_results

        dates_list = list([])
        for doc in docs_of_interest:
            dates_list.append(doc[mongoDateType])

        ''' Time Series '''
        # a list of "1" to count the docs
        ones = [1] * len(dates_list)
        # the index of the series
        idx = pd.DatetimeIndex(dates_list)
        # the actual series (at series of 1s for the moment)
        time_series = pd.Series(ones, index=idx)
        print("Time Series Head")
        print(time_series.head())

        # Resampling / bucketing
        per_day = time_series.resample('1D').sum().fillna(0)
        print("\nPer Day Time Series")
        print(per_day.head())

        s = pd.DataFrame(per_day)
        print("\nPer Day DataFrame")
        print(s.head())

        return s

    # ---------------------------------------------------------------------------------------------------------------- #


    def time_series_analysis_per_month(self, mongoDateType='mongoDate', entity_type=''):
        """ Collects all the information from the collection and presents the number of blocked IP's per day
            Saves the results in csv and json file respectively for later process (stakeholders and Highcharts)
            @param
                db:     (Mongo Client)  this is the connection returned by Pymongo Client,
                                        we take it from connect_to_mongodb() function
        """

        num_of_docs_in_collection = self.__collection.count()

        # process data if the collection only if it's not empty
        # if it empty return no analysis can be done
        if num_of_docs_in_collection == 0:
            try:
                raise Warning("No documents retrieved. Collection {} seems to be empty".format(self.__collection.name))
            except Exception as e:
                print("DescriptiveAnalysis > time_series_analysis_per_month: ", e)
            return None

        if entity_type in ['IP', 'URL', 'Domain']:
            docs_of_interest = list([])
            for doc in self.__query_results:
                if doc["Entity-Type"] == entity_type:
                    docs_of_interest.append(doc)
        # in any other case entity-type is considered as an empty string by default
        # so the whole collection is retrieved
        else:
            docs_of_interest = self.__query_results

        dates_list = list([])
        for doc in docs_of_interest:
            dates_list.append(doc[mongoDateType])

        ''' Time Series '''
        # a list of "1" to count the docs
        ones = [1] * len(dates_list)
        # the index of the series
        idx = pd.DatetimeIndex(dates_list)
        # the actual series (at series of 1s for the moment)
        time_series = pd.Series(ones, index=idx)
        print("Time Series Head")
        print(time_series.head())

        # Resampling / bucketing
        per_month = time_series.resample('1M').sum().fillna(0)
        print("\nPer Month Time Series")
        print(per_month.head())

        s = pd.DataFrame(per_month)
        print("\nPer Month DataFrame")
        print(s.head())

        return s

    # ---------------------------------------------------------------------------------------------------------------- #


    def __high_charts_timestamp__(self, datetime_obj):
        """ This is a post processing function. It receives a pandas datetime element and takes care of producing
            a timestamp suitable for high charts
            @param
                datetime_obj            (datetime)
            @returns
                __high_charts_timestamp__   (timestamp)     readable by high charts
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

    # -----------------------------------------------------------------------------------------------------------------#


    def data_frame_to_csv(self, data_frame, analysis_file_name):

        try:
            data_frame.to_csv(self.__path + '{}.csv'.format(analysis_file_name))
        except Exception as e:
            print("DescriptiveAnalysis > dataframe_to_csv : Store in CSV file Error: ", e)

    # ---------------------------------------------------------------------------------------------------------------- #


    def data_frame_to_json(self, data_frame, analysis_file_name):
        """ Given a data_frame creates a list of smaller lists that contain data frame pairs and stores them in a json file
            @param
                data_frame
                filename:   (str)   the name of the json file to be created
        """
        json_analysis_file_name = self.__path + '{}.json'.format(analysis_file_name)

        data_frame_list = list([])

        try:
            # break down every data frame row in tuple
            for row in data_frame.itertuples():
                # then keep the necessary stuff, the index timestamp and the accumulated value
                # row[0] is the datetime
                # row[1] is the number_of_attacks

                highcharts_timestamp = self.__high_charts_timestamp__(row[0])

                row_list = [highcharts_timestamp, row[1]]
                # append each list in a top list
                data_frame_list.append(row_list)

            # save list of lists in the file
            with open(json_analysis_file_name, 'w') as json_file:
                json.dump(data_frame_list, json_file, indent=4)
        except Exception as e:
            print("DescriptiveAnalysis > dataframe_to_json : Store in JSON file Error: ", e)

    # -----------------------------------------------------------------------------------------------------------------#

    def top_n(self, n, key, barplot_file_name=''):
            """
            @param
                dataset_name    (string)        the name of the data set to be created WITHOUT EXTENSION (.csv, .json)
                n               (integer)       the number of first entities to be returned
            """



            # aggregate categories
            type_of_attacks = list([])
            try:
                for doc in self.__query_results:
                    type_of_attacks.append(doc[key])

                # find most common
                results = Counter(type_of_attacks).most_common(n)

                # typecast tuples in lists
                highcharts_results = list([])
                for result in results:
                    # result is updated in results and later used
                    highcharts_results.append(list(result))
                # if filename is not specified don't create files just return the results
                if barplot_file_name == '':
                    return  highcharts_results

                ''' Store in files for Bar Plot'''
                json_barplot = self.__path + '{}.json'.format(barplot_file_name)
                csv_barplot = self.__path + '{}.csv'.format(barplot_file_name)

                # now results is a list of lists adequate for Highcharts barplot

                with open(json_barplot, 'w') as json_file:
                    json.dump(highcharts_results, json_file, separators=(',', ': '), indent=4)

                with open(csv_barplot, 'w') as csv_file:
                    for result in highcharts_results:
                        line = str(result[0]) + str(',') + str(result[1]) + str("\n")
                        csv_file.write(line)

                return highcharts_results
            except Exception as e:
                print("ExportCollectionData > topn_to_json: Store in JSON file Error: ", e)
                return None

    # -----------------------------------------------------------------------------------------------------------------#
