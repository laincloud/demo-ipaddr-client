#!/usr/bin/env python
# -*- coding: utf-8

import os
import re
import json
import requests
from flask import Flask

p = re.compile(r'.*inet (.*\..*\..*\..*)\/.*')
app = Flask(__name__)

def get_service_ip_list():
    url = 'http://ipaddr:10000/'
    r = requests.get(url)
    return r.json()

def get_resource_ip_list():
    url = 'http://ipaddr-r:10000/'
    r = requests.get(url)
    return r.json()

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
    service = get_service_ip_list()
    resource = get_resource_ip_list()
    ip_list = get_ip_list()
    r = {"client_ip": ip_list}
    try:
        resource_ip = resource.get('service_ip')
    except:
        resource_ip = []
    try:
        service_ip = service.get('service_ip')
    except:
        service_ip = []
    r['resource_ip'] = resource_ip
    r['service_ip'] = service_ip
    return json.dumps(r)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='10000')
