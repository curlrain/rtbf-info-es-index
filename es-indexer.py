__author__ = 'fabienngo'

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import json
from datetime import datetime
import re

index_name = 'rtbf-infos'
type_name = 'article'

def config():
    return """{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "analysis": {
            "filter": {
                "french_elision": {
                    "type": "elision",
                    "articles": [
                        "l",
                        "m",
                        "t",
                        "qu",
                        "n",
                        "s",
                        "j",
                        "d",
                        "c",
                        "jusqu",
                        "quoiqu",
                        "lorsqu",
                        "puisqu"
                    ]
                },
                "french_stop": {
                    "type": "stop",
                    "stopwords": "_french_"
                },
                "french_stemmer": {
                    "type": "stemmer",
                    "language": "light_french"
                }
            },
            "analyzer": {
                "french": {
                    "tokenizer": "standard",
                    "filter": [
                        "french_elision",
                        "lowercase",
                        "french_stop",
                        "french_stemmer"
                    ]
                }
            }
        },
        "mappings": {
            "article": {
                "properties": {
                    "textualContent": {
                        "type": "string",
                        "index": "analyzed",
                        "analyzer": "french"
                    },
                    "title": {
                        "type": "string",
                        "index": "analyzed",
                        "analyzer": "french"
                    },
                    "header": {
                        "type": "string",
                        "index": "analyzed",
                        "analyzer": "french"
                    },
                    "keywords": {
                        "type": "string",
                        "index": "analyzed",
                        "analyzer": "french"
                    },
                    "url": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "date": {
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
    }
}"""



HostName = 'localhost'
port = '9200'
ES = Elasticsearch(HostName + ':' + port, timeout=5)

ES.indices.create(index=index_name, body=config())
with open('res/indices/rtbf_info_prod_index.json', 'r') as file:
    data = json.load(file)

data
for id, doc_representation in data.items():
    ES.index(body=doc_representation, index=index_name, doc_type=type_name, id=id)

query_template = {
  "query": {
    "bool": {
      "should": {
        "multi_match": {
          "query": "attaque terroriste verviers",
          "type": "cross_fields",
          "fields": [
            "title^2",
            "textualContent^0.75",
            "keywords",
            "header^1.5"
          ],
          "minimum_should_match": "75%"
        }
      }
    }
  }
}

response = ES.search(index=index_name, doc_type=type_name, body=query_template)
response["hits"]['hits']

