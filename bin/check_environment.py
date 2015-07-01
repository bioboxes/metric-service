#!/usr/local/bin/python

import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(path, '..', 'src'))

import util

def check_environment_var(key):
    val = util.environment_var(key)
    print "Required environment variable present {} - {}".format(key, val)

map(check_environment_var,
        ['AWS_ACCESS_KEY', 'AWS_SECRET_KEY', 'AWS_SIMPLEDB_NAME'])
