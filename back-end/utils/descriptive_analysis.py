"""
    descriptive analysis - Utility functions to work with:
                                - mongoDB's result cursors
                                - pandas' DataFrames
                           Also contains as set of auxiliary internal functions and external routines

    Members:

        # time_series_analysis              -   performs time series analysis and returns a series DataFrame.
                                                Corresponds each date with a number of attacks that happened
        # time_series_analysis_per_month    -   performs time series analysis and returns a series DataFrame.
                                                Corresponds each MONTH with a number of attacks that happened
        # __high_charts_timestamp__         -   post processes a datetime object and converts it to be suitable for
                                                Javascript's Highcharts library
        # __high_charts_timestamp_to_date__     reverse function of __high_charts_timestamp__. Returns a date in string
                                                format.
        # __analysis_data_frame_to_dict__   -   converts DataFrames to a dictionary with key-value dictionary entries
        # __analysis_list_to_dict__         -   converts DataFrames to a dictionary with key-value dictionary entries
        # update_time_series_analysis_files -   merges analysis Datarames from file and DataFrames produced after the
                                                last crawling. Then saves them in json and csv format files
        # top_n                             -   finds and returns the most common values for a given key along with the
                                                number of appearances
        # today_datetime                    -   calculates the first and last valid datetime objects for the day
                                                provided
"""

from collections import Counter
import pandas as pd
from datetime import date, datetime
import json


def time_series_analysis(results_cursor, mongo_date_type='mongoDate', entity_type=None):
    """ Given a cursor that contains a query result set, this function performs time series analysis and returns
        the result data frame.
        @parameters
            results_cursor      (cursor)    pymongo's result cursor. It is returned by a query
            mongo_date_type     (str)       this parameter sets the datetime object based on which will take place the
                                            time series analysis. Could be 'mongoDate' or 'mongoDate-CTI'.
            entity_type         (str)       this is a special case ONLY for RANSOMWARE attacks. It can be 'IP' or 'URL'
                                            or 'Domain' to narrow down and specify which records will be analyzed
        @returns
            s        (pandas data frame)    this data frame could be empty or contains a number of attacks for each day
    """

    print("\nBegin Descriptive Analysis Phase... ", end='')

    # process data if the collection is not empty
    if results_cursor.count() == 0:
        try:
            raise Warning("No documents retrieved")
        except Exception as e:
            print("\ndescriptive_analysis module > time_series_analysis: ", e)
        # return an empty DataFrame
        s = pd.DataFrame()
        return s

    if entity_type in ['IP', 'URL', 'Domain']:
        docs_of_interest = list([])
        for doc in results_cursor.rewind():
            if doc["Entity-Type"] == entity_type:
                docs_of_interest.append(doc)
    else:
        # in any other case entity-type is an empty string by default
        # so the whole collection is retrieved
        docs_of_interest = [doc for doc in results_cursor.rewind()]

    # aggregate dates
    dates_list = list([])
    for doc in docs_of_interest:
        dates_list.append(doc[mongo_date_type])

    ''' Time Series '''
    # a list of "1" to count the docs
    ones = [1] * len(dates_list)
    # the index of the series
    idx = pd.DatetimeIndex(dates_list)
    # the actual series (at series of 1s for the moment)
    time_series = pd.Series(ones, index=idx)
    # re-sampling / bucketing
    per_day = time_series.resample('1D').sum().fillna(0)
    # results data frame
    s = pd.DataFrame(per_day)

    print('\tCompleted')
    print('\nDescriptive Analysis Results')
    print("\nTime Series Head")
    print(time_series.head())
    print("\nPer Day Time Series")
    print(per_day.head())
    print("\nPer Day DataFrame")
    print(s.head(), "\n")

    return s

    # -----------------------------------------------------------------------------------------------------------------#


def time_series_analysis_per_month(results_cursor, mongo_date_type='mongoDate', entity_type=None):
    """ Given a cursor that contains a query result set, this function performs time series analysis and returns
        the result data frame for analysed number of attacks per month.
        @parameters
            results_cursor      (cursor)    pymongo's result cursor. It is returned by a query
            mongo_date_type     (str)       this parameter sets the datetime object based on which will take place the
                                            time series analysis. Could be 'mongoDate' or 'mongoDate-CTI'.
            entity_type         (str)       this is a special case ONLY for RANSOMWARE attacks. It can be 'IP' or 'URL'
                                            or 'Domain' to narrow down and specify which records will be analyzed
        @returns
            s        (pandas data frame)    this data frame could be empty or contains a number of attacks for each day
    """

    print("\nBegin Descriptive Analysis Phase... ", end='')

    # process data if the collection is not empty
    if results_cursor.count() == 0:
        try:
            raise Warning("No documents retrieved")
        except Exception as e:
            print("\ndescriptive_analysis module > time_series_analysis: ", e)
        # return an empty DataFrame
        s = pd.DataFrame()
        return s

    if entity_type in ['IP', 'URL', 'Domain']:
        docs_of_interest = list([])
        for doc in results_cursor.rewind():
            if doc["Entity-Type"] == entity_type:
                docs_of_interest.append(doc)
    else:
        # in any other case entity-type is an empty string by default
        # so the whole collection is retrieved
        docs_of_interest = [doc for doc in results_cursor.rewind()]

    # aggregate dates
    dates_list = list([])
    for doc in docs_of_interest:
        dates_list.append(doc[mongo_date_type])

    ''' Time Series '''
    # a list of "1" to count the docs
    ones = [1] * len(dates_list)
    # the index of the series
    idx = pd.DatetimeIndex(dates_list)
    # the actual series (at series of 1s for the moment)
    time_series = pd.Series(ones, index=idx)
    # re-sampling / bucketing
    per_month = time_series.resample('1M').sum().fillna(0)
    # results data frame
    s = pd.DataFrame(per_month)

    print('\tCompleted')
    print('\nDescriptive Analysis Results')
    print("\nTime Series Head")
    print(time_series.head())
    print("\nPer Month Time Series")
    print(per_month.head())
    print("\nPer Month DataFrame")
    print(s.head(), "\n")

    return s

    # -----------------------------------------------------------------------------------------------------------------#


def __high_charts_timestamp__(datetime_obj):
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
        object. It is the reverse function of __high_charts_timestamp__.
            @parameters
                high_charts_timestamp   (timestamp)     readable by high charts library
            @returns
                                        (string)

        """
    dt = datetime.fromtimestamp(highcharts_timestamp/1000)

    return datetime(dt.year, dt.month, dt.day).strftime("%Y-%m-%d")

    # ---------------------------------------------------------------------------------------------------------------- #

def __analysis_data_frame_to_dict__(data_frame):
    """ Given a data_frame creates a dictionary that contains corresponded key-value pairs
        @parameter
            data_frame         (DataFrame)  a pandas object
            filename           (str)        the name of the json file to be created
        @returns
            data_frame_dict    (dict)       a dictionary where keys are highchart timestamps and values the number of
                                            attack incidents
    """

    data_frame_dict = dict()

    # break down every data frame row in tuple
    for row in data_frame.itertuples():
        # row[0] is the datetime            (index)
        # row[1] is the number_of_attacks   (value)
        highcharts_timestamp = __high_charts_timestamp__(row[0])

        data_frame_dict[highcharts_timestamp] = row[1]

    return data_frame_dict

    # -----------------------------------------------------------------------------------------------------------------#


def __analysis_list_to_dict__(data_list):
    """ Given a data_list (list of sublists) it creates dictionary with key-value dictionary entries
        @parameter
            data_list    (list)
        @returns
            dict_list    (list)
    """
    dictionary = dict()

    for incident in data_list:
        # index 0: timestamp,    index 1: num of attacks
        dictionary[incident[0]] = incident[1]

    return dictionary

    # -----------------------------------------------------------------------------------------------------------------#


def update_time_series_analysis_files(attacks_data_frame, analysis_file_name, path):
    """ This function transforms data from two different sources and combines them to produce a merged result. This
        result is then saved in a file. The first source is attacks data_frame (contains one or more data frames) that
        gets transformed into a dictionary. The second source is the analysis_file_name.JSON that gets tranformed into a
        dictionary too. Now that both sources are represented with the same dictionary structure it is easy to be merged
        by keys. The merged result is then represented into list of lists and saved to analysis_file_name (both
        json and csv), so can be read by highcharts.

    @parameters
        attacks_data_frame      (pandas data frame)    this data frame contains a number of attacks for each day
        analysis_file_name      (str)                  the name of analysis file (with NO EXTENSION)
        path                    (str)                  path of the analysis file
    """

    if attacks_data_frame.empty:
        try:
            raise Warning("No documents in cursor to be written")
        except Exception as e:
            print("descriptive_analysis module > update_time_series_analysis_files: ", e)
        return

    # analysis content results to dictionary
    analysed_attacks_dict = __analysis_data_frame_to_dict__(attacks_data_frame)

    # load content from analysis file (perdayTimeSeriesAnalysis)
    json_file_analysis = path + analysis_file_name + '.json'
    csv_file_analysis = path + analysis_file_name + '.csv'

    try:
        with open(json_file_analysis, 'r') as file:
            file_loaded_attacks = json.loads(file.read())
            # turn data in dictionary representation
        file_loaded_attacks_dict = __analysis_list_to_dict__(file_loaded_attacks)

        # merge contents
        for key, value in analysed_attacks_dict.items():
            file_loaded_attacks_dict[key] = value

        updated_attacks_dict = file_loaded_attacks_dict

        # back to list of lists representation for high charts
        updated_attacks_list = list([])
        for key, value in updated_attacks_dict.items():
            updated_attacks_list.append([key, value])
    except Exception as e:
        print("descriptive_analysis module > update_analysis_files > File not found and will be configured: ", e)
        updated_attacks_list = list([])
        for key, value in analysed_attacks_dict.items():
            updated_attacks_list.append([key, value])

    '''At Feb-2019 a bug occured with visualisation Highchart due to unsorted records. Sorting list is applied
    as a solution.'''
    updated_attacks_list.sort(key=lambda x: x[0])

    print('\nBegin writing results to ' + analysis_file_name + '.json and ' + analysis_file_name + '.csv...', end='')
    # write json file
    try:
        with open(json_file_analysis, 'w') as json_file:
            json.dump(updated_attacks_list, json_file, separators=(',', ': '), indent=4)
    except Exception as e:
        print("descriptive_analysis module > update_analysis_files > Store in JSON file Error: ", e)

    # write csv file
    try:
        with open(csv_file_analysis, 'w') as csv_file:
            for result in updated_attacks_list:
                # highcharts timestamp must be converted in date before saved to csv. External use NCSR Demokritos
                date_notation = __high_charts_timestamp_to_date__(result[0])
                csv_file.write(str(date_notation) + str(',') + str(result[1]) + str("\n"))
    except Exception as e:
        print("descriptive_analysis module > update_analysis_files > Store in CSV file Error: ", e)

    print('\tCompleted')

    # -----------------------------------------------------------------------------------------------------------------#


def top_n(results_cursor, n, key, barplot_file_name, path):
    """ It calculates the frequency of appearance for values of a given key in query result.
        Then returns the top n most common values with the number of appearance.
        This result gets stored in json and csv files but also gets returned by the function.
        @parameters
            dataset_name        (string)        the name of the data set to be created WITHOUT EXTENSION (.csv, .json)
            n                   (integer)       the number of first entities to be returned
            key                 (str)           the field in mongoDB's to base the analysis on
            barplot_file_name   (str)
            path                (str)           the path of file to be saved
        @returns
            highcharts_results  (list)          a list of sublists. In each sublist the first element is a value and the
                                                second is the number of attacks
    """

    # aggregate categories
    type_of_attacks = list([])
    try:
        for doc in results_cursor.rewind():
            type_of_attacks.append(doc[key])

        # find most common, results example [('Unknown', 6631), ('China', 1339), ('Russian Federation', 614)]
        results = Counter(type_of_attacks).most_common(n)

        # typecast tuples in lists
        highcharts_results = list([])
        for result in results:
            # result is updated in results and later used, highcharts_results example
            # [['Unknown', 6631], ['China', 1339], ['Russian Federation', 614], ['United States', 364]]
            # now results will be a list of lists adequate for Highcharts Barplot
            highcharts_results.append(list(result))

        # store in files for bar plot
        json_barplot = path + barplot_file_name + '.json'
        csv_barplot = path + barplot_file_name + '.csv'

        # files will be overwritten
        with open(json_barplot, 'w') as json_file:
            json.dump(highcharts_results, json_file, separators=(',', ': '), indent=4)

        with open(csv_barplot, 'w') as csv_file:
            for result in highcharts_results:
                line = str(result[0]) + str(',') + str(result[1]) + str("\n")
                csv_file.write(line)

        return highcharts_results

    except Exception as e:
        print("descriptive_analysis module > top_n > Store in file Error: ", e)
        return None

    # -----------------------------------------------------------------------------------------------------------------#


def today_datetime(utc_now):
    """ This function returns the datetime limits for a given UTC datetime
        @parameters
            utc_now         (datetime)  the datetime to be based on
        @returns
            today_start:    (datetime)  the first moment of current day
            today_end:      (datetime)  the last moment of current day
    """

    today_start = datetime(utc_now.year, utc_now.month, utc_now.day, 0, 0, 0)
    today_end = datetime(utc_now.year, utc_now.month, utc_now.day, 23, 59, 59)

    return today_start, today_end
