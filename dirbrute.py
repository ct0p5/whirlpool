#!/usr/bin/env python
# coding: utf-8

import threading
import Queue
import libs.requests as requests
import config


class Dirbrute(threading.Thread):
    def __init__(self, scan_target, scan_status, scan_timeout, urllist, name):
        super(Dirbrute, self).__init__()
        self.name = name
        self.scan_target = scan_target
        self.scan_status = scan_status
        self.scan_timeout = scan_timeout
        self.urllist = urllist
        self.load_headers()

    def run(self):
        # print 'Start Thread' + self.name
        self.scan()

    def load_headers(self):
        self.headers = {
            'Accept': '*/*',
            'Referer': self.scan_target,
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }

    def response_code(self):
        if self.scan_status == 1:
            pass
        elif self.scan_status == 2:
            self.scan_status = 403

    def scan(self):
        while not self.urllist.empty():
            self.scan_url = self.scan_target + self.urllist.get()
            try:
                r = requests.get(self.scan_url, timeout=self.scan_timeout, headers=self.headers, allow_redirects=False)
                # print r.url
                if r.status_code == 200 or r.status_code == self.scan_status:
                    print '[' + str(r.status_code) + ']' + " " + r.url
            except Exception, e:
                pass


def load_dict():
    urllist = Queue.Queue()
    with open(config.directory_dict, 'r') as f:
        for line in f.readlines():
            if line.find('#') == -1 and line != '':
                urllist.put(line.strip())
    return urllist


def begin(scan_target, scan_thread, scan_status, scan_timeout):
    # url = 'http://www.example.com/'
    scan_thread = 3
    scan_status = 200
    scan_timeout = 3
    urllist = load_dict()
    print 'Scan start!'
    for i in range(scan_thread):
        t = Dirbrute(scan_target, scan_status, scan_timeout, urllist, i)
        t.start()
    t.join()
    print 'Scan done!'
    return
