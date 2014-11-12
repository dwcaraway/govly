__author__ = 'dwcaraway'

from scrapy.spider import Spider
import urlparse
import re
from scrapy.http import Request
from urlparse import urljoin
from scraper.items import BusinessItem
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.loader import ItemLoader
from urllib2 import urlopen

def get_redirected_url(original):
        try:
            return urlopen(original).geturl()
        except Exception:
            return None

uid_matcher = re.compile("#map_canvas_(\d+)\s")

class BusinessLoader(ItemLoader):

    default_item_class = BusinessItem
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

    category_in = MapCompose(unicode.strip, lambda x: x.split('More ')[1].lower())
    image_urls_in = MapCompose(unicode.strip, lambda x: x if x.startswith('http') else urljoin('http://www.daytonlocal.com/', x))
    twitter_in = MapCompose(get_redirected_url)
    facebook_in = MapCompose(get_redirected_url)


def get_uid_from_href(href):
    """Extracts the 'id' query string parameter value from the supplied href string"""
    parsed_href = urlparse.urlparse(href)
    uid = urlparse.parse_qs(parsed_href.query)['id'][0]
    return uid

class DaytonLocalSpider(Spider):
    name = "dayton_local"
    allowed_domains = ["daytonlocal.com"]
    start_urls = [
        "http://www.daytonlocal.com/directory.asp"
    ]

    def parse(self, response):
        links = response.css('#MainContentArea div.clearc a').xpath('@href').extract()
        links = filter(lambda a: a!= u'#top', links)
        return [Request(url=link, callback=self.paginate) for link in links if not link.startswith('#')]

    def paginate(self, response):
        links = response.xpath("//div[contains(@class,'dright')]/a/ @href").extract()
        link_req_objs = [Request(url=link, callback=self.extract) for link in links]
        next_url = response.xpath("//a[text()='Next']/@href").extract()
        if next_url:
            link_req_objs.append(Request(url=urlparse.urljoin(response.url, next_url[0]), callback=self.paginate))

        return link_req_objs

    def extract(self, response):
        """
        Takes the data out of the pages at www.daytonlocal.com/listings/*
        """
        source_data_id = None

        raw_text = response.css('div.GoAwy div.clearl style').extract()
        if(len(raw_text) > 0):
            #Use the style element to find the uid using the map_canvas_(somenumber)
            r = uid_matcher.search(raw_text[0])
            source_data_id = r.groups()[0]
        else:
            #If business has a website link over their logo, grab the id
            resp_href = response.css('div.dright a').xpath('@href').extract()
            if resp_href:
               source_data_id = get_uid_from_href(resp_href[0])

        items = []

        for container in response.css('div.vcard'):
            l = BusinessLoader(selector=container)
            l.add_xpath('legalName', './div[@class="fn"]/a/strong/text()')
            l.add_xpath('image_urls', '//*[@id="MainContentArea"]//div[contains(@class, "dright")]/a/img/ @src')
            l.add_value('data_url', unicode(response.url))
            l.add_xpath('website', './div[@class="fn"]/a/@href')
            l.add_xpath('addressLocality', './/span[@class="locality"]/text()')
            l.add_xpath('addressRegion', './/span[contains(@class, "region")]/text()')
            l.add_xpath('postalCode', './/span[contains(@class, "postal-code")]/text()')
            l.add_xpath('facebook', ".//a[@class='ebutt' and contains(@href, 'lnk=fb')]/@href")
            l.add_xpath('twitter', ".//a[@class='ebutt' and contains(@href, 'lnk=tw')]/@href")
            l.add_xpath('streetAddress', './/span[contains(@class, "street-address")]/text()')
            l.add_xpath('streetAddress', './/div[@class="adr"]/br[2]/preceding-sibling::text()[1]')
            l.add_xpath('telephone', './/div[@class="clearl"]/i/following-sibling::text()[1]')
            l.add_xpath('description','.//div[@class="clearl"][2]/text()')
            l.add_xpath('category', './/div[@class="clearl"]/a[@class="ibutt"]/text()')
            l.add_value('data_uid', source_data_id)

            items.append(l.load_item())

        return items

if __name__ == '__main__':
    #Run data extraction test on individual page
    urls = ['http://www.daytonlocal.com/listings/gounaris-denslow-abboud.asp',
            'http://www.daytonlocal.com/listings/indian-ripple-dental.asp',
            'http://www.daytonlocal.com/listings/dayton-gastroenterology.asp'
            'http://www.daytonlocal.com/listings/dayton-parent-magazine.asp',
            'http://www.daytonlocal.com/listings/decoy-art-studio.asp'
            ]
    import requests
    from scrapy.http import Request, HtmlResponse

    for url in urls:
        request = Request(url=url)
        response = HtmlResponse(url=url, request=request, body=requests.get(url).text, encoding='utf-8')

        print DaytonLocalSpider.extract(DaytonLocalSpider(), response=response)

