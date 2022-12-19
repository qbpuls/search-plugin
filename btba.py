# VERSION: 1.0
# AUTHORS: apuyuseng
# CONTRIBUTORS: btba
import re
from urllib.parse import quote, unquote, urljoin
try:
    from novaprinter import prettyPrinter
except:
    from pprint import pprint as prettyPrinter

import requests
from lxml.html import fromstring


class btba(object):
    name = 'BT吧'
    url = 'https://www.aibtba.com/'

    def __init__(self) -> None:
        self.sessoin = requests.Session()
        self.sessoin.headers = {
            'referer': 'https://www.clmp4.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        self.magnet = re.compile('magnet:.*')

    def parse_search(self, html, detail, name):
        doc = fromstring(html)
        for li in set(doc.xpath('//div[@class="btdown"]/ul/li')):
            link = li.xpath('a/@href')[0]
            did, hash =  link.split('/')[-2:]
            
            downlink = self.sessoin.post(
                'https://torrent.baidu.com.btba.xiaoeryi.com/download_quick',
                data={
                    'did':did,
                    'hash':hash.strip('.html')
                },
                headers={
                    'referer': 'https://www.aibtba.com/',
                    'content-type': 'application/x-www-form-urlencoded'
                }
                )
            magnet = downlink.json()['magnet']
            size = li.xpath('b/text()')[0]
            name = li.xpath('a/text()')[0]
            self.entery_show(
                name, magnet, detail, size, -1
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
        link = urljoin('https://so.aibtba.com/', '?wd=' + quote(unquote(what)))

        html = self.sessoin.get(link).text
        doc = fromstring(html)
        
        
        for item in doc.xpath('//ul/li/div/h3'):
            if '可下载' not in item.xpath('b/text()'):
                continue
            
            detail_url = item.xpath('a/@href')[0]
            name = item.xpath('a/text()')[0]
            
            try:
                html = self.sessoin.get(detail_url).text
                self.parse_search(html, detail_url, name)
            except:
                pass
            


# btba().search('小黄人')
