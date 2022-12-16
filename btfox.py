#VERSION: 1.0
# AUTHORS: apuyuseng
# CONTRIBUTORS: btfox
import re
from urllib.parse import quote, unquote,urljoin
from novaprinter import prettyPrinter
from helpers import *


class btfox(object):
    name = "btfox"
    url = 'https://mk.btfox.pw/'

    supported_categories = {'all':'' }
    
    def parse_search(self, html):
        htmls = html.split('layui-collapse search-comar')[1:]
        for node in htmls:
            name = re.findall('<a href="(.*?)" title="(.*?)">', node)
            if not name:
                continue
                
            id, name = name[0]
            link = 'magnet:?xt=urn:btih:%s'%id.split('/')[-1].strip()
            leech = re.findall('资源热度：.*(\d+)', node)[0]
            size = re.findall('文件大小.*>(\d+[\.\w ]+)<', node)[0]
            src='https://mk.btfox.pw'+id
            self.entery_show(name, link, src,size, leech)

        
    
        
    def entery_show(self, name, link, src,size, leech):
        prettyPrinter(
            dict(
                size=size.replace(' ',''),
                link=link.strip(),
                name=name.strip(),
                leech=leech,
                seeds=-1,
                engine_url=self.url,
                desc_link=src
            )
        )

    def search(self, what, cat='all'):
        link = 'https://cache.btfox.pw/search?word=%s'%quote(unquote(what))
        headers['referer']=link
        html = retrieve_url(link)
        self.parse_search(html)
        
        for i in range(4):
            link = ('https://cache.btfox.pw/search?word=%s'%quote(unquote(what)))+'&page=%s'%(i+2)
            headers['referer']=link
            html = retrieve_url(link)
            self.parse_search(html)


if __name__ == '__main__':
    eztv_se = btfox()
    eztv_se.search('步兵', 'all')