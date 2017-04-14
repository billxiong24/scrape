"""scrape using kat57 api"""
import sys
import kat57

def main(argv=None):
    """main method"""
    if len(argv) < 3:
        print "Usage: url, folder name, file base name, number of pages (optional)"
        exit(1)

    url = argv[0]
    folder_name = argv[1]
    file_base = argv[2]
    print "Scraping url: " + url
    print "Writing to folder: " + folder_name
    print "----------------------------------------------------------------------"

    count = 0
    url_base = "http://www.theplace2.ru"
    name = kat57.get_name_from_url(url)
    parser = kat57.create_parser(url)
    page_no = argv[3] if len(argv) > 3 else kat57.find_last_page(parser)

    print "Downloading " + page_no + " pages of pictures (about 30 per page)..."
    num_pics = 0
    while count < int(page_no):
        count += 1
        print "--------------------page " + str(count) + " -----------------------"

        temp = url
        url += "page" + str(count)
        parser = kat57.create_parser(url)
        print "Connecting to " + url + "..."
        url_set = kat57.scrape_urls(parser, url_base)
        num_pics += kat57.extract_images(url_base, url_set, folder_name, name, file_base)
        url = temp

    print str(num_pics) + " pictures downloaded successfully."

main(sys.argv[1:])
