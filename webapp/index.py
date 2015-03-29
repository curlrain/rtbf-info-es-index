__author__ = 'fabienngo'
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request

import datetime
import os
from elasticsearch import Elasticsearch

app = Flask(__name__)
ES_HOSTNAME = 'localhost'
ES_PORT = '9200'
ES = Elasticsearch(ES_HOSTNAME + ':' + ES_PORT, timeout=10)
RTBF_QUERY_PATH = "../res/query-templates/xfields_date_v0.json"

with open(RTBF_QUERY_PATH, 'r') as file:
    QUERY_STRING = file.read()


def get_search_result(user_query, nresult=10):
    q = QUERY_STRING.replace("%s", user_query).replace("%d", str(datetime.datetime.today().date()))

    response = ES.search(body=q, index='infos_0.3', doc_type='rtbf-info-article', size=nresult)
    hits = response['hits']['hits']
    return [hit["_source"] for hit in hits]


@app.route("/")
def index():
    searchnews = request.args.get("searchnews")
    if not searchnews:
        searchnews = request.cookies.get("last_search")
    if not searchnews:
        searchnews = "hfd"

    results_list = [[result['title'],
                     result['url'],
                     result['header'],
                     result['published_date']] for result in get_search_result(searchnews, nresult=25)]



    response = make_response(render_template("index.html", results_list=results_list))
    if request.args.get("remember"):
        response.set_cookie("last_query", "{}".format(searchnews),
                            expires=datetime.datetime.today() + datetime.timedelta(days=365))
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port, debug=True)

