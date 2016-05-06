#!/usr/bin/env python
# -*- coding: utf-8

import os
import re
import requests
from flask import Flask

p = re.compile(r'.*inet (.*\..*\..*\..*)\/.*')
app = Flask(__name__)


def get_service_ip_list():
    url = 'http://ipaddr:10000/'
    r = requests.get(url)
    return r.content


def get_resource_ip_list():
    url = 'http://ipaddr-r:10000/'
    r = requests.get(url)
    return r.content


def get_ip_list():
    ip_list = []
    var = os.popen('ip addr').read().split("\n")
    for item in var:
        m = p.match(item)
        if m:
            ipaddr = m.groups()[0]
            if not ipaddr.startswith('127.'):
                ip_list.append(ipaddr)
    return ip_list


@app.route("/")
def get_ipaddr():
    service_content = get_service_ip_list()
    resource_content = get_resource_ip_list()
    ip_list = get_ip_list()
    return 'resource ' + resource_content + '  ' + service_content + '  client ip: ' + " ".join(ip_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='10000')
