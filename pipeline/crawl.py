__author__ = 'fabienngo'
import requests
import re
import json
import lxml.html
import xxhash
import argparse
from redis import Redis
from pymongo import MongoClient

DOMAIN = 'http://www.rtbf.be/info/'
BLACK_LIST = ["archiveparmotcle_", "emissions?", "/photo/"]
_ID_KEY = '_id'
SOURCE_KEY = 'source'
HTML_KEY = 'html'
URL_KEY = 'url'


def crawl_to_db(address, url_collection, source_collection, epoch=0, maxiter=6.0):
    """

    :param address: str the first url to be crawled
    :param domain:
    :param redis_client:
    :param epoch:
    :param maxiter:
    :param is_time:
    :return:
    """

    is_member = bool(url_collection.find_one({'url': {"$eq": address}}))
    if not is_member and DOMAIN in address and epoch < maxiter:

        url_collection.save({_ID_KEY: xxhash.xxh32(address).intdigest(), URL_KEY: address})
        print(url_collection.count())
        print(source_collection.count())
        print(address)
        epoch += 1

        try:
            if any(s in address for s in BLACK_LIST) is False:
                source = requests.get(address).text
                html_dict = {_ID_KEY: address, SOURCE_KEY: source}
                source_collection.save(html_dict)
                dom = lxml.html.fromstring(source)
                for link in dom.xpath('//a/@href'):  # select the url in href for all a tags(links)
                    crawl_to_db(link, url_collection, source_collection, epoch, maxiter)
        except:
            print("couldn't connect")
            pass


def recrawl(urls_set, url_collection, source_collection):
    for url in urls_set:
        temp_dict = {_ID_KEY: xxhash.xxh32(url).intdigest(), URL_KEY: url}
        url_collection.save(temp_dict)
        print(url_collection.count())
        if any(s in url for s in BLACK_LIST) is False:
            try:
                source = requests.get(url).text
                temp_dict[SOURCE_KEY] = source
                source_collection.save(temp_dict)
                print(source_collection.count())
            except:
                pass
    return


#
# with open('res/rtbf_info_urls.txt', 'r') as file:
#     urlSet = {url[:-1] for url in file.readlines()}
#
#
# m_client = MongoClient('localhost', 27017)
# mongo_db = m_client['rtbf-info-db']
# db_source = mongo_db['source-collection']
# db_url = mongo_db['url_collection']
# recrawl(list(urlSet)[36846:], url_collection=db_url, source_collection=db_source)


c = requests.get(DOMAIN)
c.text
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, default='http://www.rtbf.be/info/',
                        help='initial url web page')
    parser.add_argument('-h', '--host', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=27017)
    parser.add_argument("-m", '--mepoch', type=int, default=3,
                        help='max number of epoch')

    args = parser.parse_args()

    mongo_client = MongoClient(host=args.host, port=args.host)
    mongo_db = mongo_client['rtbf-info-db']
    db_source = mongo_db['source-collection']
    db_url = mongo_db['url_collection']
    db_url.remove(spec_or_id=DOMAIN)
    crawl_to_db(args.url, db_url, db_source, epoch=0, maxiter=args.mepoch)

