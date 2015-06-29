import util
import pandas as pd

def fetch_metrics():
    df = pd.DataFrame(list(util.fetch_all_metrics()))
    df['value'] = df['value'].astype(int)
    df['collected'] = df['collected'].astype('datetime64')
    df = df.set_index('collected', drop = False)
    return df

def collate_by_week(df):
    axes = [pd.TimeGrouper('W'), 'container', 'repo', 'variable']
    collated =  df.groupby(axes, as_index=False).aggregate(max)
    return collated.set_index('collected')

def per_container(df):
    axes = [pd.TimeGrouper('W'), 'container', 'repo', 'variable']
    collated =  df.groupby(axes).aggregate(max)
    return df.groupby(axes).aggregate(sum)

def total(df):
    axes = [pd.TimeGrouper('W'), 'variable']
    return df.groupby(axes).aggregate(sum)

def execute():
    metrics  = collate_by_week(fetch_metrics())
    collated = {'total' : total(metrics).to_dict(),
            'per_container' : per_container(metrics).reset_index().to_dict(orient="list")}
    return collated
