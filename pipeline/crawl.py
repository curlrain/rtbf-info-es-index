__author__ = 'fabienngo'
import requests
import re
from xxhash import xxh32
import json
import lxml.html
from time import time
import argparse
import os
import sys
sys.path.append('/pipeline')
from parse import parse
# from config import url_init, url_set

URL = 'http://www.rtbf.be/info/'
DOMAIN = 'http://www.rtbf.be/info/'
URL_PREFIX = '../res/rtbf_info_urls_'
CORPUS_PREFIX = '../res/rtbf_info_corpus_'
TXT_SUFFIX = ".txt"
JSON_SUFFIX = '.json'
ID_PREFIX = "/id_"
INDEX_PREFIX = "../res/indices/rtbf_info_index_"
PATTERN = re.compile(r'[\t\r\s,]+')
START = time()
BLACK_LIST = ["archiveparmotcle_", "emissions?", "/photo/"]


def crawl(address, address_set, domain, version, epoch=0, maxiter=6.0, is_time=False):
    """
    This function crawl the web and save the source of the crawled page. Given a initial url and a domain, it opens every
    link in that page then every link in the open recursively pages if they satisfy some confitions.
    :param address: str: the url of the initial page
    :param address_set: a set of url to add the crawled page. if the page has already been scrolled it's not add
    :param domain: str: a domain where to scroll
    :param epoch: int: serve to stop the recursion
    :param file: str: the path of the text file where to save the result
    :param maxiter: int
    :return:
    """

    if address not in address_set and domain in address and epoch < maxiter:
        address_set.add(address)
        print(len(address_set))
        print(address)
        print(epoch)
        if is_time:
            end = time()
            epoch = end - START
        else:
            epoch += 1
        try:
            with open(URL_PREFIX + version + TXT_SUFFIX, 'a') as f:
                f.write(address + "\n")
        except:
            print("IOError : counldn't save file urls in " + URL_PREFIX + version + TXT_SUFFIX)
        try:
            connection = requests.get(address)
            dom = lxml.html.fromstring(connection.text)

            if any(s in address for s in BLACK_LIST) is False:
                document = parse(address, connection.text)
                json_string = json.dumps(document, indent=4)
                with open(INDEX_PREFIX + version + ID_PREFIX + str(xxh32(address).intdigest()) + JSON_SUFFIX, "w") as f:
                    f.write(json_string)

            for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
                crawl(link, address_set, domain, version, epoch, maxiter, is_time)
        except:
            print("IOError : counldn't save file in " + URL_PREFIX + version)
            pass
    else:
        return address_set

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--url', type=str, default='http://www.rtbf.be/info/',
                        help='initial url web page',
                        )
    #
    # parser.add_argument('-s', '--set', type=str, default='http://www.rtbf.be/info/',
    #                     help='web domain to be considered for crawling')

    parser.add_argument('-s', '--set', action='store_true',
                        help='if activated a file containing urls already crawled must be given')

    parser.add_argument('-f', '--file', type=str,
                        help='the file with urls already crawled')

    parser.add_argument('-v', '--version', type=str, default="0",
                        help='version number. Give a version number to the output files')

    parser.add_argument("-t", '--time', action='store_true',
                        help='if added consider the execution time as stopping condition for the recursion')

    parser.add_argument("-m", '--mepoch', type=float, default=3,
                        help='max number of epoch')

    args = parser.parse_args()
    if args.set:
        with open(args.file, 'r') as f:
            url_set = set(f.readlines())
    else:
        url_set = set()
    i = 0
    os.mkdir(INDEX_PREFIX + args.version)
    crawled_set = crawl(args.url,
                        url_set,
                        DOMAIN,
                        epoch=0,
                        version=args.version,
                        maxiter=args.mepoch,
                        is_time=args.time)

