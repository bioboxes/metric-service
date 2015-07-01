#!/usr/local/bin/python

import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(path, '..', 'src'))

import collate
collate.execute()
