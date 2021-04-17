import json
import csv


class ExportCollectionData:
    """ This class offers all the necessary functionality to export data from a MongoDB collection and store them
        in files with various formats. End "users" of these files may be visualization libraries such as Highcharts,
        other programs or webpage's end users.
    """

    def __init__(self, collection, path):
        """
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
            projection = {"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0}

        try:
            cursor = self.__collection.find(query, projection)
            for doc in cursor:
                self.__query_results.append(doc)
            documents_retrieved = len(self.__query_results)
        except Exception as e:
            print("ExportCollectionData > __call__ : Query MongoDB Error: ", e)
            documents_retrieved = None

        return documents_retrieved

    # -----------------------------------------------------------------------------------------------------------------#

    def export_collection_to_json(self, dataset_name, entity_type=''):
        """ The function is responsible for storing collections or "portion" of a collection's data in a JSON File.
            Name of the produced file is specified as parameter with no extension and entity-type is a special case
            for retrieving only selected data.
        @param
            dataset_name    (string)    the name of the data set to be created WITHOUT EXTENSION (.csv, .json)
            entity_type     (string)    the entity type of the saved data. It is used in some cases such us ransomware
                                        collection where must be separated by entity type and saved in different files
                                        For all other collection default is an empty string ''.
                                        Values 'IP', 'URL' or 'Domain' only
        @returns
            number_of_docs_interest
                    (integer or None)   a count of docs stored in json
        """

        json_filename = self.__path + '{}.json'.format(dataset_name)

        if entity_type in ['IP', 'URL', 'Domain']:
            docs_of_interest = list([])
            for doc in self.__query_results:
                if doc["Entity-Type"] == entity_type:
                    docs_of_interest.append(doc)
        # in any other case entity-type is considered as an empty string by default
        # so the whole collection is retrieved
        else:
            docs_of_interest = self.__query_results

        try:
            ''' Store in json file '''
            with open(json_filename, 'w') as json_file:
                json.dump(docs_of_interest, json_file, separators=(',', ': '), indent=4)
            # count documents
            number_of_docs_inserted = len(docs_of_interest)

        except Exception as e:
            print("ExportCollectionData > export_collection_to_json : Store in JSON file Error: ", e)
            number_of_docs_inserted = None

        return number_of_docs_inserted

    # -----------------------------------------------------------------------------------------------------------------#

    def export_collection_to_csv(self, dataset_name, csv_header, entity_type=''):
        """ The function is responsible for storing collections or "portion" of a collection's data in a CSV File.
            Name of the produced file is specified as parameter with no extension and entity-type is a special case
            for retrieving only selected data.
        @param
            dataset_name    (string)    the name of the data set to be created WITHOUT EXTENSION (.csv, .json)
            csv_header      (list)      contains all the header strings to be inserted at the first row.
                                        The position of each field must be in compliance with position in dictionaries
                                        retrieved by MongoDB's collection
            entity_type     (string)    the entity type of the saved data.
                                        Caution:
                                            This field can used as default in all collections where data have the same
                                        structure.
                                            In collections with flexible schema (e.g RANSOMWARE) entity-type MUST be
                                        defined as argument 'IP', 'URL', 'Domain' or an EXCEPTION will be raised.

        @returns
            number_of_docs_interest
                    (integer or None)   a count of docs stored in csv
        """

        csv_filename = self.__path + '{}.csv'.format(dataset_name)

        ''' Store in csv file '''
        if entity_type in ['IP', 'URL', 'Domain']:
            docs_of_interest = list([])
            for doc in self.__query_results:
                if doc["Entity-Type"] == entity_type:
                    docs_of_interest.append(doc)
        # in any other case entity-type is considered as an empty string by default
        # so the whole collection is retrieved
        else:
            docs_of_interest = self.__query_results
        try:
            with open(csv_filename, "w", newline='', encoding='utf-8') as csvfile:
                # this is a sample header
                # csv_header = ["Category", "Subcategory", "Entity-Type", "Scope", entity_type, "False-Positive-Risk",
                #               "TimestampUTC", "DatetimeUTC", "TimestampUTC-CTI", "DatetimeUTC-CTI"]
                writer = csv.DictWriter(csvfile, fieldnames=csv_header)
                writer.writeheader()
                for doc in docs_of_interest:
                    writer.writerow(doc)
            # count documents
            number_of_docs_inserted = len(docs_of_interest)
        except Exception as e:
            print("ExportCollectionData > export_collection_to_csv : Store in CSV file Error: ", e)
            number_of_docs_inserted = None

        return number_of_docs_inserted

    # -----------------------------------------------------------------------------------------------------------------#
