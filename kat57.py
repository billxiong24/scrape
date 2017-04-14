"""RUDIMENTARY SCRAPING API for celebrity pics from www.theplace2.ru"""
#TODO get around auto-bot detection
#from pprint import pprint
#from socket import error as SocketError
import re
import os
import random
import string
import urllib2
from sets import Set
from bs4 import BeautifulSoup


def find_last_page(parser):
    """find last page of pics"""
    last_div = parser.find("div", {'class' : 'listalka ltop'})
    #last element is a new line for some reason, use second to last element
    return last_div.contents[-2].text

def scrape_urls(parser, url_base=""):
    """scrapes site for possible urls, adds to set"""
    imgs = parser.findAll('div', {'class' : 'pic_box'})
    url_set = Set()
    for pic in imgs:
        for child in pic.children:
            try:
                if re.search(r'.*\.html', child['href']):
                    url_set.add(url_base + child['href'])

            except (KeyError, TypeError):
                pass
    return url_set

def extract_images(url_base, url_set, folder, name, file_base="kate"):
    """extract images from list of urls, returns number of files downloaded"""
    if not os.path.exists(folder):
        os.makedirs(folder)

    count = 0
    for url in url_set:
        count += 1
        parser = create_parser(url)
        imgs = parser.findAll('img', {'alt' : name})

        if len(imgs) < 1:
            print "No pictures found."
            return count

        link = imgs[0]['src']

        print "Downloading file: " + url_base + link
        download_file(folder + "/" + file_base + random_string(16) + ".jpg", url_base + link)

    return count

def download_file(file_name, url):
    """function to download file"""
    file_ptr = open(file_name, 'wb')
    file_ptr.write(urllib2.urlopen(url).read())
    file_ptr.close()

def create_parser(url):
    """return html parser for webpage"""
    html_content = urllib2.urlopen(url).read()
    return BeautifulSoup(html_content, 'html.parser')

def random_string(length):
    """return a random string for file name"""
    pool = string.letters + string.digits
    return ''.join(random.choice(pool) for i in xrange(length))

def get_name_from_url(url):
    """given proper url, return name"""
    split_list = string.split(url, "photos")
    dashes = string.split(split_list[1], "-")
    return dashes[0][1:] + " " + dashes[1]
