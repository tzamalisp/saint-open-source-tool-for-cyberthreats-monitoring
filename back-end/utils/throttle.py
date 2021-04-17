from urllib.parse import urlparse
import time

# adds a delay between downloads to the same domain
class Throttle:

   def __init__(self, delay):
       self.delay = delay
       self.domains = {}

   def wait(self, url):
       domain = urlparse(url).netloc
       last_accessed = self.domains.get(domain)

       if self.delay > 0 and last_accessed is not None:
           sleep_secs = self.delay - (time.time() - last_accessed)
           if sleep_secs > 0:
                # domain has been accessed time
                # so need sleep
                time.sleep(sleep_secs)
        # update the last accessed time
       self.domains[domain] = time.time()
