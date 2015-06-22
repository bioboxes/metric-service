#!/usr/bin/env python

import yaml
import sys
import datetime
import time
import hashlib
import os

timestamp = datetime.datetime.utcnow().isoformat("T") + "Z"
seconds   = int(time.time())

with open(sys.argv[1], 'r') as f:
    metrics = yaml.load(f.read())

def create_entry((name, downloads)):
    repo, container = name.split("/")
    item = {'container' : container,
           'repo'      : repo,
           'variable'  : 'downloads',
           'value'     : downloads,
           'collected' : timestamp}
    key = hashlib.sha256(str(seconds) + name).hexdigest()
    return [key, item]

def upload(entries):
    import boto.sdb
    conn = boto.sdb.connect_to_region('us-west-1',
      aws_access_key_id     = os.environ['AWS_ACCESS_KEY'],
      aws_secret_access_key = os.environ['AWS_SECRET_KEY'])
    domain = conn.get_domain('bioboxes-container-metrics')
    domain.batch_put_attributes(entries)

upload(dict(map(create_entry, metrics)))
