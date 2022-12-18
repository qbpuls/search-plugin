#VERSION: 1.0
# AUTHORS: apuyuseng
# CONTRIBUTORS: yinfans
import re
from urllib.parse import quote, unquote
from novaprinter import prettyPrinter
from helpers import headers

DETIAL_URL = re.compile('class="thumbnail".*href="(https://www.yinfans.me/movie/\d+)"')

def retrieve_url(url,charset = 'utf-8',method='GET', data=None):
    try:
        import requests
        return requests.request(method=method, url=url, headers=headers).text
    except:
        pass
   
class yinfans(object):
    name = "4k蓝光原盘"
    url = 'https://www.yinfans.me/'

    def parse_search(self, html, detail):
        items = re.findall('href="(magnet:.*?)".*?>([\d\.GiBTMK ]+)<.*?<b>(.*?)<', html)
        for item in items:
            link, size, name = item
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
        link = 'https://www.yinfans.me/?s=%s' % quote(
            unquote(what))
        
        headers['referer'] = self.url
        html = retrieve_url(link)
        links = re.findall('href="(.*?)" class="zoom"', html)

        for url in links:
            headers['referer'] = link
            html = retrieve_url(url)
            self.parse_search(html, url)
            
            
yinfans().search('肖')