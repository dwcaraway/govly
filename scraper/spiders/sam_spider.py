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

csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

sam_fieldnames = ['DUNS', 'DUNS+4', 'CAGE CODE', 'DODAAC', 'SAM EXTRACT CODE', 'PURPOSE OF REGISTRATION', 'REGISTRATION DATE', 'EXPIRATION DATE', 'LAST UPDATE DATE', 'ACTIVATION DATE', 'LEGAL BUSINESS NAME', 'DBA NAME', 'COMPANY DIVISION', 'DIVISION NUMBER', 'SAM ADDRESS 1', 'SAM ADDRESS 2', 'SAM CITY', 'SAM PROVINCE OR STATE', 'SAM ZIP/POSTAL CODE', 'SAM ZIP CODE +4', 'SAM COUNTRY CODE', 'SAM CONGRESSIONAL DISTRICT', 'BUSINESS START DATE', 'FISCAL YEAR END CLOSE DATE', 'CORPORATE URL', 'ENTITY STRUCTURE', 'STATE OF INCORPORATION', 'COUNTRY OF INCORPORATION', 'BUSINESS TYPE COUNTER', 'BUS TYPE STRING', 'PRIMARY NAICS', 'NAICS CODE COUNTER', 'NAICS CODE STRING', 'PSC CODE COUNTER', 'PSC CODE STRING', 'CREDIT CARD USAGE', 'CORRESPONDENCE FLAG', 'MAILING ADDRESS LINE 1', 'MAILING ADDRESS LINE 2', 'MAILING ADDRESS CITY', 'MAILING ADDRESS ZIP/POSTAL CODE', 'MAILING ADDRESS ZIP CODE +4', 'MAILING ADDRESS COUNTRY', 'MAILING ADDRESS STATE OR PROVINCE', 'GOVT BUS POC FIRST NAME', 'GOVT BUS POC MIDDLE INITIAL', 'GOVT BUS POC LAST NAME', 'GOVT BUS POC TITLE', 'GOVT BUS POC ST ADD 1', 'GOVT BUS POC ST ADD 2', 'GOVT BUS POC CITY ', 'GOVT BUS POC ZIP/POSTAL CODE', 'GOVT BUS POC ZIP CODE +4', 'GOVT BUS POC COUNTRY CODE', 'GOVT BUS POC STATE OR PROVINCE', 'GOVT BUS POC U.S. PHONE', 'GOVT BUS POC U.S. PHONE EXT', 'GOVT BUS POC NON-U.S. PHONE', 'GOVT BUS POC FAX U.S. ONLY', 'GOVT BUS POC EMAIL ', 'ALT GOVT BUS POC FIRST NAME', 'ALT GOVT BUS POC MIDDLE INITIAL', 'ALT GOVT BUS POC LAST NAME', 'ALT GOVT BUS POC TITLE', 'ALT GOVT BUS POC ST ADD 1', 'ALT GOVT BUS POC ST ADD 2', 'ALT GOVT BUS POC CITY ', 'ALT GOVT BUS POC ZIP/POSTAL CODE', 'ALT GOVT BUS POC ZIP CODE +4', 'ALT GOVT BUS POC COUNTRY CODE', 'ALT GOVT BUS POC STATE OR PROVINCE', 'ALT GOVT BUS POC U.S. PHONE', 'ALT GOVT BUS POC U.S. PHONE EXT', 'ALT GOVT BUS POC NON-U.S. PHONE', 'ALT GOVT BUS POC FAX U.S. ONLY', 'ALT GOVT BUS POC EMAIL ', 'PAST PERF POC POC  FIRST NAME', 'PAST PERF POC POC  MIDDLE INITIAL', 'PAST PERF POC POC  LAST NAME', 'PAST PERF POC POC  TITLE', 'PAST PERF POC ST ADD 1', 'PAST PERF POC ST ADD 2', 'PAST PERF POC CITY ', 'PAST PERF POC ZIP/POSTAL CODE', 'PAST PERF POC ZIP CODE +4', 'PAST PERF POC COUNTRY CODE', 'PAST PERF POC STATE OR PROVINCE', 'PAST PERF POC U.S. PHONE', 'PAST PERF POC U.S. PHONE EXT', 'PAST PERF POC NON-U.S. PHONE', 'PAST PERF POC FAX U.S. ONLY', 'PAST PERF POC EMAIL ', 'ALT PAST PERF POC FIRST NAME', 'ALT PAST PERF POC MIDDLE INITIAL', 'ALT PAST PERF POC LAST NAME', 'ALT PAST PERF POC TITLE', 'ALT PAST PERF POC ST ADD 1', 'ALT PAST PERF POC ST ADD 2', 'ALT PAST PERF POC CITY ', 'ALT PAST PERF POC ZIP/POSTAL CODE', 'ALT PAST PERF POC ZIP CODE +4', 'ALT PAST PERF POC COUNTRY CODE', 'ALT PAST PERF POC STATE OR PROVINCE', 'ALT PAST PERF POC U.S. PHONE', 'ALT PAST PERF POC U.S. PHONE EXT', 'ALT PAST PERF POC NON-U.S. PHONE', 'ALT PAST PERF POC FAX U.S. ONLY', 'ALT PAST PERF POC EMAIL ', 'ELEC BUS POC FIRST NAME', 'ELEC BUS POC MIDDLE INITIAL', 'ELEC BUS POC LAST NAME', 'ELEC BUS POC TITLE', 'ELEC BUS POC ST ADD 1', 'ELEC BUS POC ST ADD 2', 'ELEC BUS POC CITY ', 'ELEC BUS POC ZIP/POSTAL CODE', 'ELEC BUS POC ZIP CODE +4', 'ELEC BUS POC COUNTRY CODE', 'ELEC BUS POC STATE OR PROVINCE', 'ELEC BUS POC U.S. PHONE', 'ELEC BUS POC U.S. PHONE EXT', 'ELEC BUS POC NON-U.S. PHONE', 'ELEC BUS POC FAX U.S. ONLY', 'ELEC BUS POC EMAIL', 'ALT ELEC POC BUS POC FIRST NAME', 'ALT ELEC POC BUS POC MIDDLE INITIAL', 'ALT ELEC POC BUS POC LAST NAME', 'ALT ELEC POC BUS POC TITLE', 'ALT ELEC POC BUS ST ADD 1', 'ALT ELEC POC BUS ST ADD 2', 'ALT ELEC POC BUS CITY ', 'ALT ELEC POC BUS ZIP/POSTAL CODE', 'ALT ELEC POC BUS ZIP CODE +4', 'ALT ELEC POC BUS COUNTRY CODE', 'ALT ELEC POC BUS STATE OR PROVINCE', 'ALT ELEC POC BUS U.S. PHONE', 'ALT ELEC POC BUS U.S. PHONE EXT', 'ALT ELEC POC BUS NON-U.S. PHONE', 'ALT ELEC POC BUS FAX U.S. ONLY', 'ALT ELEC POC BUS EMAIL ', 'NAICS EXCEPTION COUNTER', 'NAICS EXCEPTION STRING', 'DELINQUENT FEDERAL DEBT FLAG', 'EXCLUSION STATUS FLAG', 'SBA BUSINESS TYPES COUNTER', 'SBA BUSINESS TYPES STRING', 'NO PUBLIC DISPLAY FLAG', 'DISASTER RESPONSE COUNTER', 'DISASTER RESPONSE STRING', 'END OF RECORD INDICATOR']

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
