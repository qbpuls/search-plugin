# VERSION: 1.0
# AUTHORS: apuyuseng
# CONTRIBUTORS: bugutv
import re
from urllib.parse import quote, unquote, urljoin
try:
    from novaprinter import prettyPrinter
except:
    from pprint import pprint as prettyPrinter

import requests
from lxml.html import fromstring


class bugutv(object):
    name = '布谷TV'
    url = 'https://www.bugutv.net/'

    def __init__(self) -> None:
        self.sessoin = requests.Session()
        self.sessoin.headers = {
            'referer': 'https://www.clmp4.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        self.magnet = re.compile('magnet:.*')

    def parse_search(self, html, detail):
        doc = fromstring(html)
        for a in set(doc.xpath('//a[contains(@href,"magnet:?xt")]')):
            link = a.attrib['href']
 
            name = a.xpath('../text()')[0]
            size = (re.findall('[\d\.GBTKi]+', name) or [''])[0]
            self.entery_show(name, link, detail, size, -1)
            

    def entery_show(self, name, link, src, size, leech):
        prettyPrinter(
            dict(
                size=size.replace(' ', ''),
                link=link.strip(),
                name=name.strip(),
                leech=leech,
                seeds=-1,
                engine_url=self.url,
                desc_link=src
            )
        )

    def search(self, what, cat=None):
        link = 'https://www.bugutv.net/?cat=&s='+ quote(unquote(what))
        html = self.sessoin.get(link).text
        doc = fromstring(html)

        for detail_url in doc.xpath('//h2[@class="entry-title"]/a/@href'):
            print(detail_url)
            try:
                html = self.sessoin.get(detail_url).text
                self.parse_search(html, detail_url)
            except:
                pass


# bugutv().search('小黄人')
