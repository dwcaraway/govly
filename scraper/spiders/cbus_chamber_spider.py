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

class BusinessLoader(ItemLoader):

    default_item_class = BusinessItem
    default_input_processor = MapCompose(unicode, unicode.strip)
    default_output_processor = TakeFirst()

    city_in = MapCompose(unicode.strip, lambda x: x.rstrip(','))
    logo_in = MapCompose(unicode.strip, lambda x: x if x.startswith('http') else urljoin('http://web.columbus.org/', x))

class CbusChamberSpider(Spider):
    """Spider for Columbus, OH Chamber of Commerce business index"""
    name = "cbus_chamber"
    allowed_domains = ["columbus.org"]

    #Create list of starting urls
    start_urls = [
        "http://web.columbus.org/allcategories"
    ]

    def parse(self, response):
        """This will extract links to all categorized lists of businesses"""

        category_links = response.xpath('//li[@class="ListingCategories_AllCategories_CATEGORY"]/a/ @href').extract()
        category_names = response.xpath('//li[@class="ListingCategories_AllCategories_CATEGORY"]/a/ text()').extract()

        requests = []
        for category_link, category_name in zip(category_links, category_names):
            full_url = urljoin(base=response.url, url=category_link)
            requests.append(Request(url=full_url,
                                    meta={'item': BusinessItem(category=category_name)},
                                    callback=self.extract))

        return requests

    def extract(self, response):
        """This extracts part of the information and then calls a child page to extract the rest of the business info"""

        items = []

        for container in response.xpath("//div[contains(concat(' ', @class, ' '), ' ListingResults_All_CONTAINER ')]"):
#            detail_url = container.xpath('.//span[@itemprop="name"]/a/ @href').extract()[0]

            l = BusinessLoader(item = response.meta.get('item'), selector=container, response=response)
            l.add_xpath('legalName', './/span[@itemprop="name"]/a/ text()')

            street = response.xpath('.//span[@itemprop="street-address"]/ text()').extract()[0]
            addrs = street.split(', ')

            l.add_value('streetAddress', addrs[0])

            if len(addrs) > 1:
                l.add_value('streetAddress', addrs[1])

            l.add_xpath('addressLocality', './/span[@itemprop="locality"]/ text()')
            l.add_xpath('addressRegion', './/span[@itemprop="region"]/ text()')
            l.add_xpath('postalCode', './/span[@itemprop="postal-code"]/ text()')
            l.add_xpath('telephone', ".//div[contains(concat(' ', @class, ' '), 'PHONE')]/ text()")
            l.add_xpath('image_urls', ".//img[contains(concat(' ', @class, ' '), 'LOGOIMG')]/ @src")
            l.add_value('data_url', response.url)

            item = l.load_item()

            log.msg('business details extracted from index: {0}'.format(item), log.DEBUG)

            items.append(item)

        return items
