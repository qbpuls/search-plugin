# VERSION: 1.0
# AUTHORS: apuyuseng
# CONTRIBUTORS: clmp4
import re
from urllib.parse import quote, unquote, urljoin
try:
    from novaprinter import prettyPrinter
except:
    from pprint import pprint as prettyPrinter

import requests    
from lxml.html import fromstring


class clmp4(object):
    name = "磁力电影天堂"
    url = 'https://www.clmp4.com/'
    def __init__(self) -> None:
        self.sessoin = requests.Session()
        self.sessoin.headers = {
            'referer': 'https://www.clmp4.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        self.magnet = re.compile('magnet:.*')
    
    def parse_search(self, html, detail, name):
        doc = fromstring(html)
        for tr in doc.xpath('//table/tbody/tr/td/a[@href="javascript:;"]'):
            if tr.attrib['data-url'].startswith('ed2k:'):
                continue
            self.entery_show(tr.attrib['data-name'].strip('下载'),
                             tr.attrib['data-url'],
                             detail,
                             '',
                             -1
                             )
            

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
        link = urljoin(self.url, 
                'index.php?g=home&m=search&a=api&sid=1&limit=10&wd='+ quote(unquote(what)
                ))
        
        data = self.sessoin.get(link).json()['data']

        for item in data:
            detail_url = urljoin(self.url, item['link'])
            try:
                html = self.sessoin.get(detail_url).text
                self.parse_search(html, detail_url, item['name'])
            except:
                pass

clmp4().search('小黄人')