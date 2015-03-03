__author__ = 'dwcaraway'

from scrapy.spider import Spider
from scrapy import Request
from scrapy.contrib.loader import ItemLoader
from urlparse import urljoin
from items import BusinessItem
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy import log
from scrapy.shell import inspect_response
import re
import csv
from zipfile import ZipFile
try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

import json



class BusinessLoader(ItemLoader):

    default_item_class = BusinessItem
    default_input_processor = MapCompose(unicode, unicode.strip)
    default_output_processor = TakeFirst()

def get_start_urls():
    """The Sam.gov website uses AJAX and is complicated to scrape, so we just guess the filename"""

    from datetime import date
    from urllib2 import urlopen, URLError

    ret = []

    url_base = 'https://www.sam.gov/SAMPortal/extractfiledownload?role=WW&version=SAM&filename=SAM_PUBLIC_MONTHLY_'

    today = date.today()

    for x in range(1, today.day+1):
        url = "{0}{1}.ZIP".format(url_base, date(today.year, today.month, x).strftime("%Y%m%d"))
        try:
            urlopen(url)
            return [url]
        except URLError:
            continue

class SamSpider(Spider):
    """
    Spider for the General Service Administration's System for Award Management.

    This spider will download the daily extracts, parse and ingest the data and update the business records
    here in or create new ones if they do not exist.

    """
    name = "sam"
    allowed_domains = ["sam.gov"]

    #Create list of starting urls
    start_urls = get_start_urls()

    def parse(self, response):
        """This will extract links to all categorized lists of businesses"""

        #See tab 2 on https://www.sam.gov/sam/transcript/SAM%20Master%20Extract%20Mapping%20v5.1%20Public%20File%20Layout.xlsx


        filename = re.search('([a-zA-Z0-9_-]*)\.ZIP', response.url).group(1)
        fp = StringIO(response.body)

        with ZipFile(fp, 'r') as z:
            with z.open('{}.dat'.format(filename)) as f:

                for business in csv.DictReader(f, fieldnames=sam_fieldnames, dialect='piper'):

                    if not business['LEGAL BUSINESS NAME'] and business['DUNS']:
                        continue

                    l = BusinessLoader()
                    l.add_value('legalName', business['LEGAL BUSINESS NAME'])
                    l.add_value('duns', business['DUNS'])
                    l.add_value('dunsPlus4', business['DUNS+4'])
                    l.add_value('naics', business['PRIMARY NAICS'])
                    l.add_value('cage', business['CAGE CODE'])
                    l.add_value('streetAddress', business['SAM ADDRESS 1'])
                    l.add_value('streetAddress', business['SAM ADDRESS 2'])
                    l.add_value('addressLocality', business['SAM CITY'])
                    l.add_value('addressRegion', business['SAM PROVINCE OR STATE'])
                    l.add_value('postalCode', business['SAM ZIP/POSTAL CODE'])
                    l.add_value('website', business['CORPORATE URL'])
                    l.add_value('record', json.dumps(business))
                    l.add_value('record_type', u'sam')
                    l.add_value('data_uid', business['CAGE CODE'])
                    l.add_value('data_url', u'http://www.sam.gov')

                    yield l.load_item()
