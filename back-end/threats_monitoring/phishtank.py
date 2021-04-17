import time
from datetime import datetime
import itertools
from pymongo import MongoClient
from downloader import Downloader
from descriptive_analysis import *
from export_collection_data import *
# scraping libraries
from bs4 import BeautifulSoup
from lxml.html import fromstring


ts = datetime.utcnow().timestamp()
valueDt = datetime.fromtimestamp(ts)
dateTimeMongo = valueDt.strftime('%Y-%m-%d %H:%M:%S')
dateTimeMongoUTC = datetime.utcnow()

# -------------------------------------------------------------------------------------------------------------------- #


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
    try:
        soup = BeautifulSoup(html, 'lxml')
    except Exception as e:
        print(e)
        return None
    #soup = BeautifulSoup(html, 'lxml')
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

    downloader =  Downloader(delay=1,  user_agent='foskolos_lampsi', cache={})

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

    crawling_time = datetime.utcnow()
    print("Report on", crawling_time.strftime('%Y-%m-%d %H:%M:%S'), '\n')


    ''' Crawl Phishtank '''
    # parsing {0} to the string for iteration
    indicator = 'https://www.phishtank.com/phish_search.php?page={0}&active=y&verified=u'
    db = connect_to_mongodb()
    crawl_site(db, indicator)
    # -----------------------------------------------------------------------------------------------------------------#

    """ Descriptive Analysis """
    # set path of produced files
    path = '/var/www/html/saint/indicators2018/phishing/'

    # Time Series Section
    query = {}
    projection = {"_id": 0, "mongoDate": 1}
    try:
        results_cursor = db.threats.phishtank.find(query, projection)
        # create analysis file
        attack_data_frames = time_series_analysis(results_cursor, mongo_date_type='mongoDate')
        update_time_series_analysis_files(attack_data_frames,'perdayTimeSeriesPhishingCurrentInstance', path)
    except Exception as e:
        print("__main__ > Descriptive Analysis Phase > Time Series Section: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None
    # -----------------------------------------------------------------------------------------------------------------#

    """ Export Datasets """
    phishtank_csv_header = ["URL", "Submitted-by", "Valid", "Online", "DatetimeUTC", "TimestampUTC",
                            "DatetimeUTC-CTI", "TimestampUTC-CTI", "Entity-type", "Category"]
    dataset_name = 'dataset-phishing-current-instance.csv'

    print("\nRetrieving MongoDB's Collection...")
    try:
        query = {}
        projection = {"_id": 0, "mongoDate": 0, "mongoDate-CTI": 0}
        results_cursor = db.threats.phishtank.find(query, projection)
        export_to_csv(results_cursor, dataset_name, phishtank_csv_header, path)
    except Exception as e:
        print("__main__ > Export Datasets Phase: ", e)
        # destroy cursor, it won't be used again
        results_cursor = None
