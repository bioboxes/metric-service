#!/usr/local/bin/python

import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(path, '..', 'src'))

import util
import pandas as pd

def fetch_data():
    df = pd.DataFrame(list(util.fetch_all_metrics()))
    df['value'] = df['value'].astype(int)
    df['collected'] = df['collected'].astype('datetime64')
    return df
