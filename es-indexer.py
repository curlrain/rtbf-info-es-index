__author__ = 'fabienngo'

from elasticsearch import Elasticsearch
import json

index_name = 'my_index'
type_name = 'html_doc'

HostName = 'localhost'
port = '9200'
ES = Elasticsearch(HostName + ':' + port, timeout=4)

with open('res/index.json', 'r') as file:
    data = json.load(file)

for id, doc_representation in data.items():
    ES.index(body=doc_representation, index=index_name, doc_type=type_name, id=id)

query_template = {
    "query": {
        "match": {
            "text": "elasticsearch"
        }
    }
}

response = ES.search(index=index_name, doc_type=type_name, body=query_template)
response["hits"]['hits']