__author__ = 'fabienngo'
import re
from collections import defaultdict as ddict
import json
from lxml import html
# from __future__ import print_function
import argparse
import os
import glob

CORPUS_PREFIX = '../res/rtbf_info_corpus_'
INDEX_PREFIX = "../res/indices/rtbf_info_index_"
PATTERN = re.compile(r'[\t\r\s,]+')
BLACK_LIST = ["archiveparmotcle_", "emissions?", "/photo/"]


def parse(url, source):
    document_dict = ddict()
    try:
        dom = html.fromstring(source)
        document_dict['url'] = url
        try:
            document_dict["title"] = " ".join(dom.xpath('//title//text()'))
        except:
            document_dict["title"] = ""
        try:
            document_dict["header"] = " ".join(dom.xpath('//article//header//text()'))
        except:
            document_dict["header"] = ""
        try:
            keywords = dom.xpath('//article//div[@class="keywords"]//ul//text()')
            keywords = list(map(lambda x: re.sub(PATTERN, " ", x), keywords))
            keywords = list(set(filter(lambda x: x != ' ', keywords)))
            document_dict["keywords"] = keywords
        except:
            document_dict["keywords"] = []
        try:
            document_dict["textualContent"] = " ".join(dom.xpath('//article//div[@class="textualContent"]//text()'))
        except:
            document_dict["textualContent"] = ""
        try:
            raw_date = list(dom.xpath('//div[@id="mainContent"]//span[@class="date"]//text()'))
            if len(raw_date[0]) > 10:
                date = raw_date[0][:-7]
                date = re.sub(r'^\s|\s$', "", date)
                hour = raw_date[0][-5:]
                hour = re.sub(r'^\s|\s$', "", hour)
            else:
                date = raw_date
                hour = ""
            document_dict["date"] = date
            document_dict["hour"] = hour
        except:
            document_dict["date"] = ""
            document_dict["hour"] = ""
        return document_dict
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', type=str,
                        help='version number. the version number of the corpus folder')
    parser.add_argument('-o', '--output', type=str,
                        help='filename where the index is saved')

    args = parser.parse_args()
    path = CORPUS_PREFIX + args.version
    index = {'id_temp': {"key": "value"}}

    for infile in glob.glob(os.path.join(path, '*.json')):
        id = infile[len(path)+1:-5]
        with open(infile, 'r') as f:
            d = json.load(f)
            if any(s in d["url"] for s in BLACK_LIST) is False:
                index[id] = parse(d['url'], d['source'])
    del index['id_temp']
    index_json_string = json.dumps(index, indent=4)
    with open(INDEX_PREFIX + args.output + ".json", "w") as file:
        file.write(index_json_string)
    print("done")


