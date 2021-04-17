# Request library is used to Download Content using HTTP requests. Human readable and fast
import requests
from requests.exceptions import RequestException
# Custom class that ensures a "kind" rate of requests for domains
from throttle import Throttle


class Downloader:

    def __init__(self, delay=1, user_agent='saint_data', proxy=None, cache={}):
        """ __init__ method initializes a Downloader object
            @parameters
                user_agent:     (str)   user agent for request header
                cache:          (dict)  stores all downloaded
        """

        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.num_retries = None             # this variable will be set later by request (in __call__ method)
        self.proxy = proxy
        self.cache = cache
    # ---------------------------------------------------------------------------------------------------------------- #

    def __call__(self, url, num_retries=2):
        """ __call__ method downloads urls that are not found in cache or returns urls found in cache
            @parameters
               url:             (string)    web site's url
               num_retries      (int)       number
            @returns
               result['html']   (string)    web page's source code
        """

        self.num_tries = num_retries
        try:
            result = self.cache[url]
        except KeyError:
            result = None
        if result and self.num_retries and 500 <= result['code'] < 600:
            # server error so ignore result from cache
            # and re-download
            result = None

        if result is None:
            # result was not loaded from cache
            # so still need to download
            self.throttle.wait(url)
            result = self.download(url, self.user_agent, num_retries)
            if self.cache:
                # save result ot cache
                self.cache[url] = result
        return result["html_code"]

    # ---------------------------------------------------------------------------------------------------------------- #

    def download(self, url, user_agent, num_retries):
        """ This function downloads a website's source code.
            @parameters
                url             (str)       website's url
                user_agent      (str)       specifies the user_agent string
                num_retries     (int)       if a download fails due to a problem with the request (4xx) or the server
                                            (5xx) the function calls it self recursively #num_retries times
            @returns
                html_code   (str or None)   html code of web site or None if no code is returned
        """

        print("Downloading %s ... " % url)
        # set user-agent for this request
        headers = {'User-Agent': user_agent}
        try:
            resp = requests.get(url, headers=headers, proxies=self.proxy)
            # retrieve content
            html_code = resp.text
            # save the request's status code
            code = resp.status_code
            if resp.status_code >= 400:
                print('Download error:', resp.text)
                html_code = None
                if num_retries and 500 <= resp.status_code < 600:
                    # recursively retry 5xx HTTP errors
                    print("retry")
                    self.throttle.wait(url)
                    return self.download(url, user_agent, num_retries - 1)
        except RequestException as e:
            print('Download Exception error:', e)
            html_code = None
            code = e.errno

        return {'html_code': html_code, 'code': code}