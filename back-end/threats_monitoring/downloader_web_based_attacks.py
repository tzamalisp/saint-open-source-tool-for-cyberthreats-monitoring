import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
from throttle import Throttle


class Downloader:

    def __init__(self, delay=1, user_agent='saint_data', cache={}):
        """ __init__ method initializes a Downloader object
            @parameters
                user_agent:     (str)   user agent for request header
                cache:          (dict)  stores all downloaded
        """

        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.num_retries = None         # this variable will be set later by request (in __call__ method)
        self.cache = cache

    # ---------------------------------------------------------------------------------------------------------------- #

    def __call__(self, url, num_retries=2):
        """ __call__ method downloads urls that are not found in cache or returns urls found in cache
            @parameters
               url:             (string)    web site's url
               num_retries:     (int)       number
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
            result = self.download(url, self.user_agent)
            if self.cache:
                # save result ot cache
                self.cache[url] = result
        return result['html']

    # ---------------------------------------------------------------------------------------------------------------- #

    def download(self, url, user_agent, num_tries=2, charset='utf-8'):
        """ This function downloads a website's source code.
            @parameters
                url:        (str)           website's url
                user_agent: (str)           specifies the user_agent string
                num_tries:  (int)           if a download fails due to a problem with the request (4xx) or the server
                                            (5xx) the function calls it self recursively #num_tries times
                charset:    (str)           helps specify the desired codec of the HTTP responses
            @returns
                html_code:  (str or None)   html code of web site or None if no code is returned
        """

        print("Downloading %s ... " % url)
        # construct a Request object
        request = urllib.request.Request(url)
        # set user-agent for this request
        request.add_header('User-Agent', user_agent)
        try:
            # make a request and get an HTTPResponse object back
            #   response is a context manager (.info(), .getcode(), .geturl())
            response = urllib.request.urlopen(request)
            # reading response as string (bytes originally)
            # 'ignore' arg is crucial to avoid errors when decoding bytes with codec different than charset ('utf-8')
            html_code = response.read().decode(charset, 'ignore')
            response_code = response.getcode()
        except (URLError, HTTPError, ContentTooShortError) as e:
            print("Downloading Error:", e.reason)
            html_code = None
            if hasattr(e, 'code'):
                response_code = e.code
            else:
                response_code = None
            if num_tries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # recursively retry 5xx HTTP errors (server errors)
                    return self.download(url, user_agent, num_tries-1, charset)

        # Our beloved html_code is UTF-8 STRING or NONE
        # TODO(4) delete statement
        # print("HTML: {0}".format(type(html_code)))

        return {'html': html_code, 'code': response_code}