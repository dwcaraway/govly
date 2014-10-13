__author__ = 'dwcaraway'

from scrapy.spider import Spider
from scrapy import Request
from scrapy.contrib.loader import ItemLoader
from urlparse import urljoin, urlparse
from scraper.items import BusinessItem
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy import log
import string
import re
from scrapy.shell import inspect_response

class BusinessLoader(ItemLoader):

    default_item_class = BusinessItem
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

    city_in = MapCompose(unicode.strip, lambda x: x.rstrip(','))

class CincyChamberSpider(Spider):
    """Spider for Cincinnati Chamber of Commerce business index"""
    name = "cincy_chamber"
    allowed_domains = ["cincinnatichamber.com"]

    #Create list of starting urls
    start_urls = [
        "http://www.cincinnatichamber.com/search/searchforbusiness.aspx?DOSEARCH=Y&COMPNAME={0}".format(letter) for letter in string.lowercase
    ]

    def parse(self, response):
        """This will extract links to all categorized lists of businesses and return that list"""

        log.msg('Cincy chamber parse() called on url {0}'.format(response.url), log.DEBUG)

        #Check if over 500 results
        is_over_500 = len(response.xpath('//span[@id="ctl00_ctl00_body_maincontentblock_lOnlyTopCompaniesReturned"]').extract()) > 0
        if is_over_500:
            log.msg('Over 500 results for {0}'.format(response.url), log.DEBUG)
            return [Request(url=response.url+letter, callback=self.parse) for letter in string.lowercase]

        #Extract string of form 'You are viewing page 1 of 25'. Get the last number to figure out how much to paginate
        viewing_page_str = unicode.strip(response.xpath('//*[@id="ctl00_ctl00_body_maincontentblock_pnlResults"]/i/ text()').extract()[0])
        last_page= int(re.search(pattern=r"(\d+)$", string=viewing_page_str).group(1))
        return [Request(url='{0}&page={1}'.format(response.url, page), callback=self.after_parse) for page in range(0, last_page)]


    def after_parse(self, response):
        """This extracts the email, phone and website data and then calls a child page to extract the rest of the business info"""

        extraction_requests = []

        for container in response.xpath('//tr[@align="center"]'):
            detail_url = container.xpath('./td[1]/a/ @href').extract()[0]

            l = BusinessLoader(selector=container, response=response)
            l.add_xpath('phone', './td[1]/span/ text()')
            l.add_xpath('website', './td[2]/a/ @href')
            l.add_xpath('email', "substring-after(./td[4]/a/ @href,'mailto:')")
            l.add_xpath('name', './td[1]/a/ text()')
            item = l.load_item()

            log.msg('business details extracted from index: {0}'.format(item))

            extraction_requests.append(Request(url = urljoin(response.url, detail_url), meta={'item':item}, callback=self.extract))

        return extraction_requests

    def extract(self, response):
        """Extracts data from a business page"""

        #grab the BusinessItem passed in from the caller
        i = response.meta['item']

        log.msg('passed in item={0}'.format(i), log.DEBUG)

        l = BusinessLoader(item=i, response=response)

        #Assume url pattern is /<city>/<category>/<duid>/<name>.html
        data_uid = re.match(pattern=u'.*COMPANYID=(\d+)$', string=response.url).group(1).lstrip('0')

        l.add_xpath('description', '//*[@id="ctl00_ctl00_body_maincontentblock_lblProductandServices"]/ text()')

        #List of strings which, when joined, form the address. form is <address1>, <optional: address2>, <city and state and zip>
        address_fields = response.xpath('//*[@id="ctl00_ctl00_body_maincontentblock_lblcoAddress"]/ text()').extract()
        m = re.match(pattern=u'(\w+),\s+(\w+)[\xa0]+(\S+)$', string=address_fields[-1])

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
