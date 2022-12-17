"""#VERSION: 1.0
# AUTHORS: qbpuls
# CONTRIBUTORS: nexus

import re
from urllib.parse import quote, unquote,urljoin
from novaprinter import prettyPrinter
from helpers import *


NAME = re.compile('href="details.*?>(.*?)</td>')
RESID = re.compile('href="details.php\?(id=\d+)')
SIZE = re.compile('>([\d\.]+)<br />([GBMTK]+)')
SEEDERS = re.compile('#seeders">(\d+)')
LEECHERS = re.compile('#leechers">(\d+)')

def remove_tags(text, which_ones=(), keep=()):
    if which_ones and keep:
        raise ValueError('Cannot use both which_ones and keep')

    which_ones = {tag.lower() for tag in which_ones}
    keep = {tag.lower() for tag in keep}

    def will_remove(tag):
        tag = tag.lower()
        if which_ones:
            return tag in which_ones
        else:
            return tag not in keep

    def remove_tag(m):
        tag = m.group(1)
        return u'' if will_remove(tag) else m.group(0)

    regex = '</?([^ >/]+).*?>'
    retags = re.compile(regex, re.DOTALL | re.IGNORECASE)

    return retags.sub(remove_tag, text)

def retrieve_url(url,charset = 'utf-8',method='GET', data=dict()):
    req = urllib.request.Request(url, headers=headers, method=method, data=data)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as errno:
        print(" ".join(("Connection error:", str(errno.reason))))
        return ""
    dat = response.read()
    # Check if it is gzipped
    try:
        compressedstream = io.BytesIO(dat)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        extracted_data = gzipper.read()
        dat = extracted_data
    except:
        pass
    info = response.info()
    return dat.encode(charset, 'replace')
    

class {filename}:
    name = "{name}"
    url = '{url}'
    cookie ='{cookie}'
    passkey = '{passkey}'
    
    def parse_search(self, html):
        content = html.split('<table class="torrentname" width="100%">')[1:]
        for line in content:
            resId = RESID.findall(line)[0]
            prettyPrinter(
                dict(
                    size=''.join((SIZE.findall(line)[0])),
                    link=urljoin(
                        self.url, 'download.php?%s&passkey=%s' % (resId, self.passkey)),
                    name=remove_tags(NAME.findall(line)[0]),
                    
                    leech=(LEECHERS.findall(line) or [0])[0],
                    seeds=(SEEDERS.findall(line) or [0])[0],
                    engine_url=self.url,
                    desc_link=urljoin(self.url, 'details.php?%s'%resId)
                )
            )
            
    def search(self, what, cat=None):
        uri = 'torrents.php?incldead=1&spstate=0&inclbookmarked=0&search=%s&search_area=0&search_mode=0'%quote(unquote(what))
        url = urljoin(self.url, uri)
        headers['referer'] = self.url
        headers['cookie'] = self.cookie
        html = retrieve_url(url)
        self.parse_search(html)
"""
from os.path import join, abspath, dirname
from json import load
base_path = dirname(abspath(__file__))

with open(join(base_path,'nexus.json')) as f:
    settings = load(f)


for key, setting in settings.items():
    file_name = join(base_path, '%s.py'%key)
    try:
        with open(file_name, 'w') as f:
            content = __doc__.format(filename=key, **setting)
            f.write(content)
    except:
        pass