__author__ = 'fabienngo'
import requests
import lxml.html
import xxhash
# import argparse
from configparser import ConfigParser
from pymongo import MongoClient

DOMAIN = 'rtbf.be/info/'
RTBF_INFO = 'http://www.rtbf.be/info/'
BLACK_LIST = ["archiveparmotcle_", "emissions?", "/photo/"]
_ID_KEY = '_id'
SOURCE_KEY = 'source'
HTML_KEY = 'html'
URL_KEY = 'url'


def crawl_to_db(address, url_collection, source_collection, epoch=0, maxepoch=6.0):
    """

    :param address:
    :param url_collection:
    :param source_collection:
    :param epoch:
    :param maxepoch:
    :return:
    """

    is_member = bool(url_collection.find_one({'url': {"$eq": address}}))
    condition = is_member is False and DOMAIN in address and epoch < maxepoch
    if condition:
        url_collection.save({_ID_KEY: xxhash.xxh32(address).intdigest(), URL_KEY: address})
        print(url_collection.count())
        print(source_collection.count())
        print(address)
        epoch += 1

        try:
            source = requests.get(address).text
            if any(s in address for s in BLACK_LIST) is False and "#" not in address:
                html_dict = {URL_KEY: address, SOURCE_KEY: source}
                source_collection.save(html_dict)
            dom = lxml.html.fromstring(source)
            for link in dom.xpath('//a/@href'):  # select the url in href for all a tags(links)
                crawl_to_db(link, url_collection, source_collection, epoch, maxepoch)
        except:
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



if __name__ == '__main__':
    parser = ConfigParser()
    parser.read('../res/config_crawler.INI')
    #Other options url
    url_init = parser.get('Others', 'url_init')
    max_epoch = parser.getint('Others', 'epoch')
    remove_rtbf_info_url = parser.getboolean('Others', 'remove_rtbf_info_url')

    #Mongo DB options
    db_host = parser.get('MongoDB', 'hostname')
    db_port = parser.getint('MongoDB', 'port')
    db_name = parser.get('MongoDB', 'db')

    mongo_client = MongoClient(db_host, db_port)
    db = mongo_client[db_name]
    source_collection = db['source-collection']
    url_collection = db['url_collection']
    if remove_rtbf_info_url:
        url_collection.remove(spec_or_id={'url': RTBF_INFO})
    crawl_to_db(url_init, url_collection, source_collection, epoch=0, maxepoch=max_epoch)


#
# with open('res/rtbf_info_urls.txt', 'r') as file:
#     urlSet = set(file.read().split("\n"))
#
#
# recrawl(list(urlSet)[36846:], url_collection=db_url, source_collection=db_source)

#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-u', '--url', type=str, default='http://www.rtbf.be/info/',
#                         help='initial url web page')
#     parser.add_argument('-h', '--host', type=str, default='localhost')
#     parser.add_argument('-p', '--port', type=int, default=27017)
#     parser.add_argument("-m", '--mepoch', type=int, default=3,
#                         help='max number of epoch')
#
#     args = parser.parse_args()
#
#     mongo_client = MongoClient(host=args.host, port=args.host)
#     mongo_db = mongo_client['rtbf-info-db']
#     db_source = mongo_db['source-collection']
#     url_collection = mongo_db['url_collection']
#     url_collection.remove(spec_or_id=DOMAIN)
#     crawl_to_db(args.url, url_collection, db_source, epoch=0, maxiter=args.mepoch)
#
