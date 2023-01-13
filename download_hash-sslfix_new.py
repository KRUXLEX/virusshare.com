#!/usr/bin/env python
"""This script downloads all available Virusshare.com hash files. The user-agent is set to Chrome 57. It can be called
as:
./download_hashes.py PATH
or quiet as:
./download_hashes -q PATH
"""
import progressbar
import requests
import os
import sys
from bs4 import BeautifulSoup
import urllib.request

URL = 'https://virusshare.com/'
TABLEURL = "https://virusshare.com/hashes.4n6"

def run(path, quiet=False):
    """
    Downloads all available hash files to a given path.
    
    :param path: Path to download directory
    :param quiet: If set to True, no progressbar is displayed
    """
    if os.path.isdir(path):
        urls = scrap_urls()

        if not quiet:
            p = progressbar.ProgressBar(maxval=len(urls))
            p.start()

        counter = 0
        for url in urls:
            file_path = "{}/{}.md5".format(path, str(counter).zfill(3))
            if os.path.exists(os.path.join(file_path)):
                counter += 1
                continue

            try:
                urllib.request.urlretrieve(url, file_path)
            except:
                print("cannot download: {}".format(url))
            

            if not quiet:
                p.update(counter)

            counter += 1
        
    else:
        print('Given path is not a directory.')
        sys.exit(1)

def scrap_urls():
    page = requests.get(TABLEURL)

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table")

    tr = table.find('tr')
    a = tr.find_all('a')

    urls = []
    for elem in a:
        urls.append('https://virusshare.com/{}'.format(elem.attrs['href']))

    return urls

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == '-q':
        run(sys.argv[2], quiet=True)
    else:
        print('No path given')
        sys.exit(1)
