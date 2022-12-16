#VERSION: 1.0
# AUTHORS: apuyuseng
# CONTRIBUTORS: dytt8
import re
from urllib.parse import quote, unquote,urljoin
from novaprinter import prettyPrinter
from helpers import *

def retrieve_url(url,charset = 'utf-8',method='GET', data={}):
    
    """ 
    自带的编码不友好
    Return the content of the url page as a string """
    req = urllib.request.Request(url, headers=headers, method=method, data=data)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as errno:
        print(" ".join(("Connection error:", str(errno.reason))))
        return ""
    dat = response.read()
    # Check if it is gzipped
    if dat[:2] == b'\x1f\x8b':
        # Data is gzip encoded, decode it
        compressedstream = io.BytesIO(dat)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        extracted_data = gzipper.read()
        dat = extracted_data
    info = response.info()
    
    try:
        ignore, charset = info['Content-Type'].split('charset=')
    except Exception:
        pass
    
    dat = dat.decode(charset, 'replace')
    dat = htmlentitydecode(dat)
    # return dat.encode('utf-8', 'replace')
    return dat




class ygdy8(object):
    name = "电影天堂"
    url = 'https://www.dygod.net/'

    supported_categories = {
        'all':[1,2,19,16],
        'movies':[1],
        'tv':[2],
        'games':[19],
        'anime':[16],
    } 
    
    def parse_search(self, html):
        links = re.findall("(\/html/[\w\/]+\/\d+\.html)", html)
        print('搜索到数据链接', links)
        for link in links:
            link = urljoin(self.url, link)
            self.parse_detail(retrieve_url(link, 'gbk'), link)
        
    def parse_detail(self, html, src):
        '''
        retrieve_url 编码识别不准确, 对中非utf-8不友好
        故这里不再提取作品信息
        '''
        
        downlink = re.findall("(ftp:\/\/.*?)\"", html)
        for link in  downlink:
            name = unquote(link.rsplit('/')[-1]).strip()
            #self.entery_show(name, link, src)  
        
        # dn=
        downlink2 = re.findall("(magnet\:\?xt=.*?)\"", html)
        for link in  downlink2:
            name = link.rsplit('&dn=')[-1].split('&')[0]
            self.entery_show(unquote(name), link, src)  
            
        
    def entery_show(self, name, link, src):
        # print(name)
        prettyPrinter(
            dict(
                size=-1,
                link=link.strip(),
                name=name.strip(),
                leech=-1,
                seeds=-1,
                engine_url=self.url,
                desc_link=src
            )
        )

    def search(self, what, cat='all'):
        cat_keys = self.supported_categories.get(cat)
        if not cat_keys:
            return
        sk = quote(unquote(what).encode('gb2312'))
        data = 'show=title&tempid=1&keyboard=%s&Submit=%s'%(sk,'%C1%A2%BC%B4%CB%D1%CB%F7')

        html = retrieve_url('https://www.dygod.net/e/search/index.php',method='POST', data=bytes(data, 'utf8'))
        self.parse_search(html)


if __name__ == '__main__':
    eztv_se = ygdy8()
    eztv_se.search('庆余年', 'all')