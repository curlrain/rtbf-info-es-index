__author__ = 'fabienngo'
import requests
import re
from bs4 import BeautifulSoup
from xxhash import xxh32
from collections import defaultdict as ddict
import json
import lxml.html


def crawl(address, address_set, domain, iter, file, maxiter=6):
    """
    This function crawl the web and save the url of the crawled page. Given a initial url and a domain, it opens every
    link in that page then every link in the open page if they satisfy 3 confitions. It is a recursive algorithm.
    :param address: str: the url of the initial page
    :param address_set: a set of url to add the crawled page. if the page has already been scrolled it's not add
    :param domain: str: a domain where to scroll
    :param iter: int: serve to stop the recursion
    :param file: str: the path of the text file where to save the result
    :param maxiter: int
    :return:
    """
    if address not in address_set and domain in address and iter < maxiter:
        # json.dumps(address)
        address_set.add(address)
        print(len(address_set))
        print(address)
        print(iter)
        iter += 1
        try:
            connection = requests.get(address)
            dom = lxml.html.fromstring(connection.text)
            with open(file, 'a') as f:
                f.write(address + "\n")

            for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
                crawl(link, address_set, domain, iter, file, maxiter)

        except:
            print("didn't work")
            pass

    else:
        return address_set
url = 'http://www.rtbf.be/info/'
url_set = set()
domain = 'http://www.rtbf.be/info'
i = 0
crawled_set = crawl(url, url_set, domain, iter=0, file='res/rtbf_info_urls_100.txt', maxiter=100)
print('done')
crawled_set
type(crawled_set)

with open('res/rtbf_info_urls_100.txt', 'r') as f:
    content = list(f)
for el in content:
    print(el)
len(content)