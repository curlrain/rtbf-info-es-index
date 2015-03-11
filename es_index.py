__author__ = 'fabienngo'

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import json
import os, glob
from config import config
import argparse

INDEX_PREFIX = "res/indices/rtbf_info_index_"

# TODO Change this awfull UI
def es_index(path, index_name, type_name, hostname, port, is_create):
    ES = Elasticsearch(hostname + ':' + port, timeout=5)
    if is_create:
        ES.indices.create(index=index_name, body=config())
    for infile in glob.glob(os.path.join(path, '*.json')):
        with open(infile, 'r') as file:
            doc_representation = json.load(file)
            id = infile[len(path)+1:-5]
            ES.index(body=doc_representation, index=index_name, doc_type=type_name, id=id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=str,
                        help='version number. the version number of the index folder')
    parser.add_argument('--index', type=str,
                        help='the name of elasticsearch the index')
    parser.add_argument('--type', type=str,
                        help='the name of the index')
    parser.add_argument('--hostname', type=str, default='localhost',
                        help='host name')
    parser.add_argument('--port', type=str, default='9201',
                        help='port')
    parser.add_argument('--create', action="store_true")

    args = parser.parse_args()
    index_path = INDEX_PREFIX + args.version
    es_index(index_path, args.index, args.type, args.hostname, args.port, args.create)

# index_name = 'rtbf-infos-test'
# type_name = 'article'
#
# HostName = 'localhost'
# port = '9200'
#
# version = 'test'




# response = ES.search(index=index_name, doc_type=type_name, body=query_template)
# response["hits"]['hits']
