#!/usr/bin/env python

import datetime
import hashlib
import itertools as it
import json
import os
import time

import boto.sdb

timestamp = datetime.datetime.utcnow().isoformat("T") + "Z"
seconds   = int(time.time())

def fetch_page(url):
    import requests
    return requests.get(url).text


def fetch_list_of_bioboxes():
    """
    Fetches list of all bioboxes
    """
    url = "https://raw.githubusercontent.com/bioboxes/data/master/images.yml"
    raw = yaml.load(fetch_page(url))
    f = lambda x: x['image']['dockerhub']
    return set(reduce(lambda acc, x: acc + map(f,x), raw.values(), []))


def fetch_metrics_data(repo, page = 1, acc = []):
    """
    Collect container metrics from docker hub repository
    """
    url = "https://registry.hub.docker.com/v2/repositories/{}/?page={}"
    metrics = json.loads(fetch_page(url.format(repo, page)))

    if metrics['next'] is not None:
        return fetch_metrics_data(repo, page + 1, acc + metrics['results'])
    else:
        return acc + metrics['results']


def create_entry(metric):
    """
    Format metrics for upload to simpledb
    """
    item = {'container' : metric['name'],
            'repo'      : metric['namespace'],
            'variable'  : 'downloads',
            'value'     : metric['pull_count'],
            'collected' : timestamp}
    key = hashlib.sha256(str(seconds) + metric['name']).hexdigest()
    return [key, item]


def container_repo(container):
    """
    Get the repository of a container
    """
    return container.split("/")[0]


def generate_metrics():
    containers   = fetch_list_of_bioboxes()
    repositories = set(map(container_repo, containers))
    metrics =  filter(
            lambda x: x['namespace'] + "/" + x["name"] in containers,
            it.chain(*map(fetch_metrics_data, repositories)))
    return map(create_entry, metrics)


def upload((key, entry)):
    conn = boto.sdb.connect_to_region('us-west-1',
      aws_access_key_id     = os.environ['AWS_ACCESS_KEY'],
      aws_secret_access_key = os.environ['AWS_SECRET_KEY'])
    domain = conn.get_domain('bioboxes-container-metrics')
    domain.put_attributes(key, entry)


metrics = generate_metrics()
map(upload, metrics)
print "Completed processing {} entries at {}".format(len(metrics), timestamp)
