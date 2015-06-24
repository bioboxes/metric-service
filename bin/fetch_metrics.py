#!/usr/bin/env python

from lxml import html
import yaml
import json

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


def container_repo(container):
    """
    Get the repository of a container
    """
    return container.split("/")[0]

containers = fetch_list_of_bioboxes()
repositories = set(map(container_repo, containers))
metrics = reduce(lambda y, x: y + x, map(fetch_metrics_data, repositories))

filter(lambda x: x['namespace'] + "/" + x["name"] in containers, metrics)
print yaml.safe_dump(metrics)
