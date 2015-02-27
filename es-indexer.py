__author__ = 'fabienngo'

from elasticsearch import Elasticsearch
import json
from datetime import datetime
import re

index_name = 'rtbf-infos'
type_name = 'article'

HostName = 'localhost'
port = '9200'
ES = Elasticsearch(HostName + ':' + port, timeout=4)

with open('res/rtbf_info_dev_index.json', 'r') as file:
    data = json.load(file)


for id, doc_representation in data.items():
    ES.index(body=doc_representation, index=index_name, doc_type=type_name, id=id)

query_template = {
    "query": {
        "match": {
            "textualContent": "Ukraine"
        }
    }
}

response = ES.search(index=index_name, doc_type=type_name, body=query_template)
response["hits"]['hits']

l = ['\t\t\r\n    \t\t',
    'Automobile',
    ',\xa0',
    '\r\n    \t\t',
    'Environnement',
    ',\xa0',
    '\r\n    \t\t',
    'Politique',
    '\r\n  \t']


['how', 'much', 'is<br/>', 'the', 'fish<br/>', 'no', 'really']
