"""scrape kate"""
#from pprint import pprint
import os
import urllib2
from bs4 import BeautifulSoup

def main():
    """main method"""
    url = "https://www.si.com/swimsuit/model/kate-upton/2017/photos"

    print "Connecting to " + url + "..."
    html_content = urllib2.urlopen(url).read()
    parser = BeautifulSoup(html_content, 'html.parser')
    imgs = parser.findAll('div', {'class' : 'media-img'})
    extract_images(imgs, "kate-upton")

def extract_images(tags, folder):
    """extract image source from tags"""
    counter = 0
    if not os.path.exists(folder):
        os.makedirs(folder)

    for child in tags:
        for test in child.contents:
            #TODO figureout issinstance
            try:
                link = test['src']
                file_ptr = open(folder + "/" + "kate" + str(counter) + ".jpg", 'wb')
                counter += 1

                print "Downloading file: " + test['src']
                file_ptr.write(urllib2.urlopen(link).read())
                file_ptr.close()

            except Exception:
                pass

main()
