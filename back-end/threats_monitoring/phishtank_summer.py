import time
from datetime import datetime
import itertools
from pymongo import MongoClient
from downloader import Downloader
from descriptive_analysis import DescriptiveAnalysis
from export_collection_data import ExportCollectionData
# scraping libraries
from bs4 import BeautifulSoup
from lxml.html import fromstring


ts = datetime.utcnow().timestamp()
valueDt = datetime.fromtimestamp(ts)
dateTimeMongo = valueDt.strftime('%Y-%m-%d %H:%M:%S')
dateTimeMongoUTC = datetime.utcnow()

# -------------------------------------------------------------------------------------------------------------------- #


def connect_to_mongodb():
    # connect to database
    connection = MongoClient('XXX.XXX.XXX.XXX', 27017)
    db = connection.admin
    db.authenticate('xxxxxx', 'xxxXXXxxxXX')

    return db

# -------------------------------------------------------------------------------------------------------------------- #


def getLinks(html):
    """ This function downloads a web page and discovers all it's links
        @param
            html        (string)    webpage 's html code
        @return
            htmlLinks   (list)      contains all the discovers links
    """

    soup = BeautifulSoup(html, 'lxml')
    possible_links = soup.find_all('a')

    htmlLinks = []

    for link in possible_links:
        if link.has_attr('href'):
            if link.attrs['href'].startswith("phish_detail.php?phish_id="):
                linkDefault = 'https://www.phishtank.com/'
                linkConnect = '{}{}'.format(linkDefault, link.attrs['href'])
                htmlLinks.append(linkConnect)
                #print(link.attrs['href'])

    return htmlLinks


# -------------------------------------------------------------------------------------------------------------------- #


def getContentItemID(url, downloader):
    """ This function receives the url of a specific phish page (ID), then finds and returns it's http host link
        @param
            url     (str)   url page of a phish attack
        @return
            contentFromList  (str)  the host page of phish attack
    """

    html = downloader(url)
    # parse html
    soup = BeautifulSoup(html, 'lxml')
    # studying the page revealed that the phish url is in bold
    valuesList = soup.find_all('b')

    if valuesList[1] != '':
        contentFromList = valuesList[1].text
    else:
        contentFromList = None


    return contentFromList


# -------------------------------------------------------------------------------------------------------------------- #


def crawl_site(db, url, max_errors=5):
    """ This is the main function for crawling Phishtank website
        @param
            db
            url
            max_errors
        @return:
    """

    num_errors = 0
    listBadLinks = []
    seenListBadLinks = set(listBadLinks)
    idIDs = []
    seenidIDs = set(idIDs)
    dictlistMongo = []

    downloader =  Downloader(delay=1,  user_agent='giorgos93', cache={})

    for page in itertools.count(0):
        pg_url = url.format(page)
        # prepare Downloader object

        # download a page
        html = downloader(pg_url)
        # parse page
        soup = BeautifulSoup(html, 'lxml')
        td = soup.find_all(attrs={'class': 'value'})

        if not td:
            print('no tables!')
            num_errors += 1
            if num_errors == max_errors:
                # reached max number of errors, so exit
                break
        elif html is None:
            num_errors += 1
            if num_errors == max_errors:
                # reached max number of errors, so exit
                break
        else:
            num_errors = 0
            # success - can scrape the result
            # CSS Selectors - XPATH
            print()
            print('Content:')

            listGetContentIDs = getLinks(html)
            # print('List with ID links')
            # print(listGetContentIDs)
            print()

            for itemList in listGetContentIDs:
                if itemList not in seenListBadLinks:
                    seenListBadLinks.add(itemList)
                    listBadLinks.append(getContentItemID(itemList, downloader))

            tree = fromstring(html)
            td = tree.cssselect('td.value')
            counter = 0

            for i in range(0, len(td), 5):
                # id
                id = td[i].text_content()
                id = int(id)

                idCheck = db.threats.phishtank.find_one({"_id": id})
                # print(idCheck)

                if idCheck is None:
                    print('Not duplicate key found! Continue..')
                else:
                    print('Duplicate key value found:', idCheck['_id'])

                # datetime
                date = td[i + 1].text_content()
                date2 = date.split()
                del date2[0:2]
                dataClean = date2[1]
                s1 = []
                for s in dataClean:
                    if s.isdigit():
                        s1.append(s)
                dataClean2 = ''.join(s1)
                date2[1] = dataClean2
                dataCleanFinal = ' '.join(date2)
                print(dataCleanFinal)

                try:
                    # valid_date = time.strptime(date, '%m/%d/%Y')
                    datetimeObjectUTC = datetime.strptime(dataCleanFinal, '%b %d %Y %I:%M %p')
                    print('datetimeObjectUTC:', datetimeObjectUTC)
                except ValueError:
                    print('Invalid date!')

                # datetimeObjectUTC = datetime.strptime(dataCleanFinal, '%b %d %Y %I:%M %p')
                datetimeUTC = datetimeObjectUTC.strftime('%Y-%m-%d %H:%M:%S')
                print('datetimeUTC:', datetimeUTC)
                timestampUTC = int(time.mktime(datetimeObjectUTC.timetuple()))

                # CTI datetime
                datetimeObjectUTCCTI = dateTimeMongoUTC
                datetimeUTCCTI = datetimeObjectUTCCTI.strftime('%Y-%m-%d %H:%M:%S')

                # CTI timestamp
                timestampUTCCTI = ts

                # author
                submitted = td[i + 2].text_content()
                if submitted != '':
                    try:
                        submitted2 = submitted.split()
                        submittedFinal = submitted2[1]
                    except IndexError as e:
                        print("Error in crawl_site(), submittedFinal: ", e)
                        submittedFinal = None
                else:
                    submittedFinal = None

                # valid
                valid = td[i + 3].text_content()
                if valid == '':
                    valid = None

                # online
                online = td[i + 4].text_content()
                if online == '':
                    online = None

                # print(datetimeUTC)

                dictionary = {}

                if id not in seenidIDs:

                    dictionary['_id'] = id
                    dictionary['URL'] = listBadLinks[counter]
                    dictionary['Submitted-by'] = submittedFinal
                    dictionary['Valid'] = valid
                    dictionary['Online'] = online
                    dictionary['TimestampUTC'] = timestampUTC
                    dictionary["mongoDate"] = datetimeObjectUTC
                    dictionary['DatetimeUTC'] = datetimeUTC
                    dictionary['TimestampUTC-CTI'] = timestampUTCCTI
                    dictionary['mongoDate-CTI'] = datetimeObjectUTCCTI
                    dictionary['DatetimeUTC-CTI'] = datetimeUTCCTI
                    dictionary['Entity-type'] = 'URL'
                    dictionary['Category'] = 'Phishing'

                    seenidIDs.add(id)
                    idIDs.append(id)
                    dictlistMongo.append(dictionary)

                    counter += 1

                # TODO: delete time.sleep()
                # time.sleep(0.5)

            print('Length of list IDs:', len(seenidIDs))
            print('Length of Mongo Dictionary:', len(dictlistMongo))
            print('next')
            print()
            print()

        # time.sleep(0.5)

    # drop collection if not empty
    if db.threats.phishtank.count() != 0:
        db.threats.phishtank.drop()
        print('Database reset')
    else:
        print('Database is empty! Starting storing data..')

    for dictionaryMongo in dictlistMongo:
        print(dictionaryMongo)
        # handle to web based attacks (1) collection
        # phishtank = db.threats.phishtank

        db.threats.phishtank.insert(dictionaryMongo)

    print()
    print("Data inserted successfully to MongoDB")
    print()
    print()
    print('The End!')

# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":

    print("Report on", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '\n')
    # parsing {0} to the string for iteration
    indicator = 'https://www.phishtank.com/phish_search.php?page={0}&active=y&verified=u'

    # ''' Crawl Phishtank'''
    db = connect_to_mongodb()
    crawl_site(db, indicator)

    """ Set Path Of Data Exportation """
    # to run on server
    server_path = '/var/www/html/saint/indicators2018/phishing/'
    # to run locally
    local_path = ""

    """ Descriptive Analysis and Result Exportation"""
    analysis = DescriptiveAnalysis(collection=db.threats.phishtank, path=server_path)
    analysis(query={}, projection={"_id": 0})
    # returns a pandas data frame
    data_frame = analysis.time_series_analysis('mongoDate')
    # store analysis results
    analysis.data_frame_to_csv(data_frame, "perdayTimeSeriesPhishingCurrentInstance")
    analysis.data_frame_to_json(data_frame, "perdayTimeSeriesPhishingCurrentInstance")

    ''' Export current MongoDB collection instance '''
    # exploitDataBase = ExportCollectionData(collection=db.threats.phishtank, path=server_path)
    # exploitDataBase(query={}, projection={"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0})
    # exploitDataBase.export_collection_to_json("dataset-phishing-current-instance")
    #
    # csv_header = ["URL", "Submitted-by", "Valid", "Online", "DatetimeUTC", "TimestampUTC",
    #                       "DatetimeUTC-CTI", "TimestampUTC-CTI", "Entity-type", "Category"]
    # exploitDataBase.export_collection_to_csv("dataset-phishing-current-instance", csv_header)
