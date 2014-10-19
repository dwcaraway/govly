__author__ = 'dwcaraway'

from scrapy.spider import Spider
from scrapy import Request
from scrapy.contrib.loader import ItemLoader
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
            meta = {'item': BusinessItem(category=category, data_uid=data_uid, data_source_url=url)}
            requests.append(Request(url=url, callback=self.extract, meta=meta))

        return requests

    def extract(self, response):
        """This extracts part of the information and then calls a child page to extract the rest of the business info"""

        l = BusinessLoader(item = response.meta.get('item'), response=response)
        l.add_xpath('name', './/span[@itemprop="name"]/a/ text()')

        street = response.xpath('.//span[@itemprop="street-address"]/ text()').extract()[0]
        addrs = street.split(', ')

        l.add_value('address1', addrs[0])

        if len(addrs) > 1:
            l.add_value('address2', addrs[1])

        l.add_xpath('city', './/span[@itemprop="locality"]/ text()')
        l.add_xpath('state', './/span[@itemprop="region"]/ text()')
        l.add_xpath('zip', './/span[@itemprop="postal-code"]/ text()')
        l.add_xpath('phone', ".//div[contains(concat(' ', @class, ' '), 'PHONE')]/ text()")
        l.add_xpath('image_urls', ".//img[contains(concat(' ', @class, ' '), 'LOGOIMG')]/ @src")

        item = l.load_item()

        log.msg('business details extracted from index: {0}'.format(item), log.DEBUG)

        items.append(item)

        return item
