__author__ = 'fabienngo'
import requests
import re
from bs4 import BeautifulSoup
from xxhash import xxh32
from collections import defaultdict as ddict
import json
from lxml import html as H
import sys
from __future__ import print_function

pattern = re.compile(r'[\t\r\s,]+')
def parse_rtbf_info(url):
    document_dict = ddict()
    try:
        connection = requests.get(url)
        dom = H.fromstring(connection.text)
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
            keywords = list(map(lambda x: re.sub(pattern, " ", x), keywords))
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
                hour = raw_date[0][-5:]
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

# testing the code on a subsample
with open('res/rtbf_info_urls.txt', 'r') as f:
    content = list(set(f))

len(content)
black_list = ["archiveparmotcle_", "emissions?", "/photo/"]

index = {"id" + str(xxh32(url).intdigest()): parse_rtbf_info(url)
         for url in content[0:20] if any(s in url for s in black_list) == False}


index_json_string = json.dumps(index, indent=4)
with open("res/rtbf_info_dev_index.json", "w") as file:
    file.write(index_json_string)
print("done")
len(index)
type(index)
for id, doc in index.items():
    # print(type(doc["title"]))
    # print(type(doc["header"]))
    # print(type(doc["textualContent"]))
    print(doc["date"])
    print("-----------------------------------")

