#!/usr/bin/env python3

import urllib.request
from enum import Enum
import time
import functools
import http.client
import random


def main():
    count = 0
    while True:
        print(vote('418')) # Dr. Tareq Suwaidan
#        print(vote('383')) # Mahdi Elmandjra
        print(vote('626')) # Dr. Ashraf Abd Al-aziz Mansour
        print(vote('378')) # Dr. Gihan Gamal
        count += 1
        print(count)
#        print(vote(''))
#        print(vote(''))
        time.sleep(90)



class status(Enum):
    Error = 0
    VoteAdded = 1
    IpUsedBefore = 2
    OtherError = 3

class NoRedirection(urllib.request.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response



def vote(id):

    response = None

    try:
        opener = urllib.request.build_opener(NoRedirection)
        urllib.request.install_opener(opener)
        req = urllib.request.Request("http://www.ichaps.org/voting/test2.php")

        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0")
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8")
        req.add_header("Accept-Language", "en-US,en;q=0.5")
        req.add_header("Accept-Encoding", "gzip, deflate")
        req.add_header("Referer", "http://www.ichaps.org/voting/medalofexcellence.php")
        req.add_header("Connection", "keep-alive")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("X-Forwarded-For", str(random.randrange(1,254)) + '.' +  str(random.randrange(1,254)) + '.' +  str(random.randrange(1,254)) + '.' + str(random.randrange(1,254)) )

        data = urllib.parse.urlencode({'trainers': id}).encode('utf-8')
        response = urllib.request.urlopen(req, data)
        if response.headers['location'] == 'erorrpage.php':
            return status.IpUsedBefore
        if response.headers['location'] == 'medalofexcellence.php':
            return status.VoteAdded        
    except urllib.error.URLError as e:
        if not hasattr(e, "code"):
            status.OtherError
        response = e
        print(e)
    except Exception as e:
        status.OtherError
        print(e)



    return status.OtherError

main()
