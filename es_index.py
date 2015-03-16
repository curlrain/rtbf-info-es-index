__author__ = 'fabienngo'

from elasticsearch import Elasticsearch
import json
from xxhash import xxh32
import sys
import argparse
from pymongo import MongoClient
sys.path.append('/Users/fabienngo/PycharmProjects/elasticsearch-index/pipeline')
from html_parser import rtbf_info_parser
from configparser import ConfigParser

BLACK_LIST = ["archiveparmotcle_", "emissions?", "/photo/"]


def es_index_collection(source_collection,
                        index_name, version, type_name,
                        hostname, port,
                        is_create, config_file,
                        htmlparser=rtbf_info_parser):
    with open('./res/settings-mappings/' + config_file, 'r') as file:
        es_config = json.loads(file.read())
    ES = Elasticsearch(hostname + ':' + port, timeout=5)
    name = index_name + "_" + version
    if is_create:
        ES.indices.create(index=name, body=es_config)

    for html_dict in source_collection.find():
        if any(s in html_dict["url"] for s in BLACK_LIST) is False:
            _id = xxh32(html_dict['url']).intdigest()
            doc = htmlparser(html_dict['url'], html_dict['source'])
            if len(doc['textualContent']) != 0:
                ES.index(body=doc, index=name, doc_type=type_name, id=_id)

# TODO define a es_index function that index only one document.

if __name__ == "__main__":

    parser = ConfigParser()
    parser.read('./res/config.INI')

    #ElasticSearch Options
    es_host = parser.get('ElasticSearch', 'hostname')
    es_port = parser.get('ElasticSearch', 'port')

    #Mongo DB options
    db_host = parser.get('MongoDB', 'hostname')
    db_port = parser.getint('MongoDB', 'port')
    db_name = parser.get('MongoDB', 'db')

    #Index options
    index_name = parser.get('Index', 'name')
    type_name = parser.get('Index', 'type')
    version = parser.get('Index', 'version')
    create = parser.getboolean('Index', 'is_create')
    config = parser.get('Index', 'config')

    mongo_client = MongoClient(db_host, db_port)
    db = mongo_client[db_name]
    collection = db['source-collection']

    es_index_collection(source_collection=collection,
                        index_name=index_name,
                        version=version,
                        type_name=type_name,
                        hostname=es_host,
                        port=es_port,
                        is_create=create,
                        config_file=config)

# index_name = 'rtbf-infos-test'
# type_name = 'article'
#
# HostName = 'localhost'
# port = '9200'
#
# version = 'test'




# response = ES.search(index=index_name, doc_type=type_name, body=query_template)
# response["hits"]['hits']
