#VERSION: 1.0
# AUTHORS: qbpuls
# CONTRIBUTORS: nexus
import re
from urllib.parse import quote, unquote,urljoin
from novaprinter import prettyPrinter
from helpers import *
from json import load


with open('nexus_settings.json', 'r') as f:
    settings = load(f)



class nexusBase(object):
    name = "qbpuls"
    url = 'https://mk.btfox.pw/'

    supported_categories = {'all':'' }
    
    def parse_search(self, html):
        # download.php?id=10353&passkey=
        htmls = html.split('<table class="torrents"')[1:]
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

    def search(self, what, cat=None):
        uri = 'torrents.php?incldead=1&spstate=0&inclbookmarked=0&search=%s&search_area=0&search_mode=0'%quote(unquote(what))
        url = urljoin(self.url, uri)
      
        headers['referer'] = self.url
        html = retrieve_url(url)
        self.parse_search(html)
        
if __name__ == '__main__':
    eztv_se = btfox()
    eztv_se.search('步兵', 'all')