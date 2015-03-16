__author__ = 'fabienngo'
import re
from collections import defaultdict as ddict
from lxml import html



PATTERN = re.compile(r'[\t\r\s,]+')
BLACK_LIST = ["archiveparmotcle_", "emissions?", "/photo/"]


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
        # try:
        #     keywords = dom.xpath('//article//div[@class="keywords"]//ul//text()')
        #     keywords = list(map(lambda x: re.sub(PATTERN, " ", x), keywords))
        #     keywords = list(set(filter(lambda x: x != ' ', keywords)))
        #     document_dict["keywords"] = keywords
        # except:
        #     document_dict["keywords"] = []
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
            document_dict["published_date"] = "".join(dom.xpath(".//meta[@property='article:published_time']/@content"))[:-14]

            # raw_date = list(dom.xpath('//div[@id="mainContent"]//span[@class="date"]//text()'))
            # if len(raw_date[0]) > 10:
            #     date = raw_date[0][1:-7]
            #     date = re.sub(r'^\s|\s$', "", date)
            #     hour = raw_date[0][-5:]
            #     hour = re.sub(r'^\s|\s$', "", hour)
            # else:
            #     date = raw_date
            #     hour = ""

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




len("T16:50:00+0100")