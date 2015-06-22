#!/usr/bin/env python

from lxml import html
import yaml

def fetch_page(url):
    import requests
    return requests.get(url).text

def fetch_download_data(repo):
    """
    Fetches numbers of container downloads for a given dockerhub repo.
    """
    url = "https://registry.hub.docker.com/repos/{}/".format(repo)
    tree = html.fromstring(fetch_page(url))
    downloads = map(int, tree.xpath('//div[@title="Number of pulls"]/div/text()'))
    names     = map(lambda x: x.strip(), tree.xpath('//h2/text()'))
    return zip(names, downloads)

def fetch_list_of_bioboxes():
    """
    Fetches list of all bioboxes
    """
    url = "https://raw.githubusercontent.com/bioboxes/data/master/images.yml"
    raw = yaml.load(fetch_page(url))
    f = lambda x: x['image']['dockerhub']
    return set(reduce(lambda acc, x: acc + map(f,x), raw.values(), []))

def container_repo(container):
    """
    Get the repository of a container
    """
    return container.split("/")[0]

containers = fetch_list_of_bioboxes()
repositories = set(map(container_repo, containers))
all_downloads = reduce(lambda acc, x: acc + fetch_download_data(x), repositories, [])

metrics = filter(lambda (x, y): x in containers, all_downloads)
print yaml.safe_dump(metrics)
