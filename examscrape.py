"""scrapes Jeffrey's stuff"""
import os
from Queue import Queue
import re
import urllib2
from bs4 import BeautifulSoup

#constants
QUEUE = Queue(maxsize=0)
URL = "https://users.cs.duke.edu/~chase/systems/"
HTML_CONTENT = urllib2.urlopen(URL).read()
PARSER = BeautifulSoup(HTML_CONTENT, 'html.parser')

def main():
    """ main method """
    traverse_dir()

def traverse_dir():
    """traverse file directory"""
    QUEUE.put("")
    while not QUEUE.empty():
        link = QUEUE.get()
        print "Entering new directory: " + URL + link
        content = urllib2.urlopen(URL + link).read()
        parser = BeautifulSoup(content, 'html.parser')
        visit_files(parser.findAll("a", href=re.compile(".*pdf$")), link)
        visit_folders(parser.findAll("a", href=re.compile("[/]$")), link)



def visit_files(files, link):
    """handles and download files"""
    for child in files:
        if link == "":
            download(URL + link + child['href'], child['href'])
        else:
            download(URL + link + child['href'], child['href'], link)

def visit_folders(folders, curr_dir):
    """handles folders appropriately"""
    for child in folders:
        #it doesn't work in regex for something reason
        if "~" in child['href']:
            continue
        QUEUE.put(curr_dir + child['href'])


def download(url, filename, folder="home"):
    """Download and write file"""

    print "Downloading " + url
    if not os.path.exists(folder):
        os.makedirs(folder)

    pdf_file = open(folder + "/" + filename, 'wb')
    pdf_file.write(urllib2.urlopen(url).read())
    pdf_file.close()

main()
