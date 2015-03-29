__author__ = 'fabienngo'
import re
from collections import defaultdict as ddict
from lxml import html


def rtbf_info_parser(url, source):
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
            document_dict['keywords'] = dom.xpath(".//meta[@name='keywords']/@content")
        except:
            document_dict['keywords'] = ''
        try:
            document_dict['news_keywords'] = dom.xpath(".//meta[@name='news_keywords']/@content")
        except:
            document_dict['news_keywords'] = ""
        try:
            document_dict["textualContent"] = " ".join(dom.xpath('//article//div[@class="textualContent"]//text()'))
        except:
            document_dict["textualContent"] = ""
        try:
            document_dict["published_date"] = "".join(dom.xpath(".//meta[@property='article:published_time']"
                                                                "/@content"))[:-14]

        except:
            pass
        try:
            document_dict["modified_date"] = "".join(dom.xpath(".//meta[@property='article:modified_time']/@content"))[:-14]

        except:
            pass
        try:
            author = dom.xpath('//article//div[@class="textualContent"]/p/strong//text()')[-1]
            document_dict['author'] = author.replace('\xa0', '')

        except:
            document_dict['author'] = ''

        return dict(document_dict)
    except:
        pass




