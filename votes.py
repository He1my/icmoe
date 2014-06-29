#!/usr/bin/env python3

import urllib.request
from enum import Enum
import netifaces as ni
from subprocess import call
import time
import functools
import http.client


def main():
    for x in range(1, 10):
        ip = ChangeIP()
        st = vote(ip)
        print(st)
        if st == status.VoteAdded or st == status.IpUsedBefore:
            with open('usedIps.txt', 'a') as myfile:
                myfile.write(ip + '\n')


def ChangeIP():
    usedIp = True
    ip = ''
    while usedIp:
        ip = restartPPPOE()
        print(ip)
        usedIp = False
        with open('usedIps.txt') as f:
            for line in f:
                if ip in line:
                    usedIp = True
                    print('network IP used before.')
                    break
    return ip


def restartPPPOE():
    call(["poff", "tedata"])
    call(["pon", "tedata"])
    ip = ''
    for x in range(1, 100):
        time.sleep(0.1)
        ip = getip()
        if ip != '':
            break
        print(x)
        if x == 10:
            print("error: unable to connect to PPPOE")
            return ''
    return ip


def getip():
    ip = ''
    try:
        ip = ni.ifaddresses('ppp0')[2][0]['addr']
    except:
        pass
    return ip


def getVotes():
    return 0



class status(Enum):
    Error = 0
    VoteAdded = 1
    IpUsedBefore = 2
    OtherError = 3

class NoRedirection(urllib.request.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response


class BoundHTTPHandler(urllib.request.HTTPHandler):

    def __init__(self, source_address=None, debuglevel=0):
        urllib.request.HTTPHandler.__init__(self, debuglevel)
        self.http_class = functools.partial(http.client.HTTPConnection, source_address=source_address)

    def http_open(self, req):
        return self.do_open(self.http_class, req)


def vote(ip):

    response = None

    try:
        handler = BoundHTTPHandler(source_address=("192.168.1.100", 0))
        opener = urllib.request.build_opener(NoRedirection, handler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request("http://www.ichaps.org/voting/test2.php")

        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0")
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8")
        req.add_header("Accept-Language", "en-US,en;q=0.5")
        req.add_header("Accept-Encoding", "gzip, deflate")
        req.add_header("Referer", "http://www.ichaps.org/voting/medalofexcellence.php")
        req.add_header("Connection", "keep-alive")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        data = b"trainers=412"
        response = urllib.request.urlopen(req, data)

    except urllib.error.URLError as e:
        if not hasattr(e, "code"):
            status.OtherError
        response = e
    except Exception as e:
        status.OtherError

    if response.headers['location'] == 'erorrpage.php':
        return status.IpUsedBefore
    if response.headers['location'] == 'medalofexcellence.php':
        return status.VoteAdded

    return status.OtherError

main()
