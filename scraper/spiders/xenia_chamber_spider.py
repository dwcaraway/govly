__author__ = 'dwcaraway'

from scrapy.spider import Spider
from scrapy import Request
from scrapy.contrib.loader import ItemLoader 
from scrapy.shell import inspect_response
from scraper.items import BusinessItem
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy import log
import re

class BusinessLoader(ItemLoader):

    default_item_class = BusinessItem
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

class XeniaChamberSpider(Spider):
    """Spider for Columbus, OH Chamber of Commerce business index"""
    name = "xenia_chamber"
    allowed_domains = ["xacc.com"]

    #Create list of starting urls
    start_urls = [
        "http://www.xacc.com/staticpages/index.php?page=member-directory"
    ]

    def parse(self, response):
        """This will extract links to all categorized lists of businesses"""

        business_nodes = response.xpath('//div[@class="bus-listing"]')

        requests = []

        for node in business_nodes:
            url = node.xpath('./strong/a/ @href').extract()[0]
            data_uid = re.match(pattern=u'.*CoID=(\d+)$', string=url).group(1).lstrip('0')
            category = node.xpath('./preceding-sibling::h2[1]/ text()').extract()[0]
            meta = {'item': BusinessItem(category=category, source_data_id=data_uid, source_url=url)}
            requests.append(Request(url=url, callback=self.extract, meta=meta))

        return requests

    def extract(self, response):
        """This extracts part of the information and then calls a child page to extract the rest of the business info"""

        l = BusinessLoader(item = response.meta.get('item'), response=response)
        l.add_xpath('legalName', '//*[@id="gl_content-wide-left"]/h1/ text()')
        l.add_xpath('streetAddress', '//*[@id="gl_content-wide-left"]/table//table//tr[1]/td[1]/text()[1]')

        city_state_zip_raw = response.xpath('//*[@id="gl_content-wide-left"]/table//table//tr[1]/td[1]/text()[2]').extract()
        if len(city_state_zip_raw) > 0:
            m = re.match('\s*(\w+\s*\w*),\s+(\w+)\s*(\d*)\s*', city_state_zip_raw[0])
            
            l.add_value('addressLocality', m.group(1))
            l.add_value('addressRegion', m.group(2))
            l.add_value('postalCode', m.group(3))

        l.add_xpath('telephone', '//*[@id="gl_content-wide-left"]/table//table//tr[1]/td[2]/text()[2]')
        l.add_xpath('latitude', '//*[@id="lat"]/ @value')
        l.add_xpath('longitude', '//*[@id="lon"]/ @value')

        item = l.load_item()

        return item
