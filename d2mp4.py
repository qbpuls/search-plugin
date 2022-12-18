# VERSION: 1.0
# AUTHORS: apuyuseng
# CONTRIBUTORS: d2mp4

import re
import requests
from urllib.parse import quote, unquote, urljoin
from lxml.html import fromstring
from novaprinter import prettyPrinter

HEADERS = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'
}

FORUMLIST = re.compile(
    '(thread-\d+.htm)'
)

NAME = re.compile('>\n(.*?)\n</h4')
ATTACH = re.compile('href="(attach-download-\d+.htm)"')
class d2mp4:
    name = '第二MP4'
    url = 'https://www.d2mp4.net/'
    
    def search(self, what, cat=None):
        key = quote(unquote(what)).replace('%','_')
        url = urljoin(self.url, 'search-%s-1.htm'%key)
        html = requests.get(url, headers=HEADERS).text
        for detail in list(set(FORUMLIST.findall(html))):
            detail = urljoin(self.url, detail)
            print(detail)
            try:
                html = requests.get(detail, headers=HEADERS).text
                self.search_parse(html, detail)
            except Exception as e:
                print(e)
                pass
            
    def search_parse(self, html, detail):
        doc = fromstring(html)
        name = doc.xpath('//h4[@class="break-all"]/text()')
        name = ''.join(name).strip()
        # 种子文件
        for node in doc.xpath('//ul[@class="attachlist"]/li/a'):
            down = node.attrib['href']
            filename = ''.join(node.xpath('text()')).strip()
            if re.findall('\.torrent$', filename, re.I):
                self.entery_show(
                    filename,
                    urljoin(self.url, down),
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
# d2mp4().search('周星驰')