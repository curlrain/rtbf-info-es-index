__author__ = 'fabienngo'
import requests
import re
from bs4 import BeautifulSoup
from xxhash import xxh32
from collections import defaultdict as ddict
import json
from lxml import html as H


def parse_rtbf_info(url):
    document_dict = ddict()
    try:
        connection = requests.get(url)
        dom = H.fromstring(connection.text)
        document_dict['url'] = url
        try:
            document_dict["title"] = dom.xpath('//title//text()')
        except:
            document_dict["title"] = ""
        try:
            document_dict["header"] = dom.xpath('//article//header//text()')
        except:
            document_dict["header"] = ""
        try:
            document_dict["keywords"] = dom.xpath('//article//div[@class="keywords"]//ul//text()')
        except:
            document_dict["keywords"] = []
        try:
            document_dict["textualContent"] = " ".join(dom.xpath('//article//div[@class="textualContent"]//text()'))
        except:
            document_dict["textualContent"] = ""
        try:
            raw_date = dom.xpath('//span//@class="date updatedNews"')
            date = raw_date[14:-8]
            hour = raw_date[-5:]
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

black_list =["archiveparmotcle_", "emissions?", "/photo/"]

index = [parse_rtbf_info(url) for url in content[0:300] if any(s not in url for s in black_list)]
len(index)
for el in index[0:10]:
    print(el["title"])
    print(el["header"])
    print(el["textualContent"])
    print("-----------------------------------")

