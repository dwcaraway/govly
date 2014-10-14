__author__ = 'dwcaraway'

from scrapy.spider import Spider
from scrapy import Request
from scrapy.contrib.loader import ItemLoader
from urlparse import urljoin
from scraper.items import BusinessItem
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy import log
from scrapy.shell import inspect_response
import re

class BusinessLoader(ItemLoader):

    default_item_class = BusinessItem
    default_input_processor = MapCompose(unicode.strip)
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

        return [Request(url=urljoin(base=response.url, url=category_links[x]), meta={'category', category_names[x]}, callback=self.after_parse) for x in range(len(category_links))]

    def after_parse(self, response):
        """This extracts part of the information and then calls a child page to extract the rest of the business info"""

        extraction_requests = []

        for container in response.xpath("//div[contains(concat(' ', @class, ' '), ' ListingResults_All_CONTAINER ')]"):
            detail_url = container.xpath('.//span[@itemprop="name"]/a/ @href').extract()[0]

            l = BusinessLoader(selector=container, response=response)
            l.add_xpath('name', './/span[@itemprop="name"]/a/ text()')
            l.add_value('category', response.meta.get('category'))

            street = response.xpath('.//span[@itemprop="street-address"]/ text()').extract()[0]
            addrs = street.split(', ')

            l.add_value('address1', addrs[0])

            if len(addrs) > 1:
                l.add_value('address2', addrs[1])

            l.add_xpath('city', './/span[@itemprop="locality"]/ text()')
            l.add_xpath('state', './/span[@itemprop="region"]/ text()')
            l.add_xpath('zip', './/span[@itemprop="postal-code"]/ text()')
            l.add_xpath('phone', ".//div[contains(concat(' ', @class, ' '), 'PHONE')]/ text()")
            l.add_xpath('logo', ".//img[contains(concat(' ', @class, ' '), 'LOGOIMG')]/ @src")

            item = l.load_item()

            log.msg('business details extracted from index: {0}'.format(item))

            extraction_requests.append(Request(url = urljoin(response.url, detail_url), meta={'item':item}, callback=self.extract))

        return extraction_requests

    def extract(self, response):
        """Extracts data from a business page"""

        #grab the BusinessItem passed in from the caller
        i = None
        try:
            i = response.meta['item']
        except Exception:
            i = BusinessItem()

        log.msg('passed in item={0}'.format(i), log.DEBUG)

        l = BusinessLoader(item=i, response=response)

        #Assume url pattern is /<city>/<category>/<duid>/<name>.html
        data_uid = re.match(pattern=u'.*COMPANYID=(\d+)$', string=response.url).group(1).lstrip('0')

        l.add_xpath('description', '//*[@id="ctl00_ctl00_body_maincontentblock_lblProductandServices"]/ text()')

        #List of strings which, when joined, form the address. form is <address1>, <optional: address2>, <city and state and zip>
        address_fields = response.xpath('//*[@id="ctl00_ctl00_body_maincontentblock_lblcoAddress"]/ text()').extract()
        m = re.match(pattern=u'^([\w\s]*),\s+([\w\s]+)[\xa0]+(\S+)$', string=address_fields[-1])

        l.add_value('address1', address_fields[0])

        if len(address_fields) is 3:
            l.add_value('address2', address_fields[1])

        l.add_value('city', m.group(1))
        l.add_value('state', m.group(2))
        l.add_value('zip', m.group(3))

        #Extract any social media links
        social_media_links = response.xpath('//table[@id="ctl00_ctl00_body_maincontentblock_gvSocialMedia"]//a/ @href').extract()
        for link in social_media_links:
            if 'linkedin.com' in link:
                l.add_value('linkedin', unicode(link))
            elif 'twitter.com' in link:
                l.add_value('twitter', unicode(link))
            elif 'facebook.com' in link:
                l.add_value('facebook', unicode(link))

        l.add_value("data_uid", unicode(data_uid))
        l.add_value("data_source_url", unicode(response.url))

        return l.load_item()
