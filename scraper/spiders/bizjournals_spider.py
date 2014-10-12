__author__ = 'dwcaraway'

from scrapy.spider import Spider
from scrapy import Request
from scrapy.contrib.loader import ItemLoader
from urlparse import urljoin
from scraper.items import BusinessItem
from scrapy.contrib.loader.processor import MapCompose
from scrapy.shell import inspect_response


class BizJournalsSpider(Spider):
    """Spider for bizjournals local business index"""
    name = "bizjournals"
    allowed_domains = ["bizjournals.com"]
    start_urls = [
        "http://businessdirectory.bizjournals.com/dayton",
        "http://businessdirectory.bizjournals.com/cincinnati",
        "http://businessdirectory.bizjournals.com/columbus",
        "http://businessdirectory.bizjournals.com/louisville"
    ]

    def parse(self, response):
        """This will extract links to all categorized lists of businesses and return that list"""

        #Categories is a list [] of URL strings
        category_links = response.xpath('//table[@class="b2Local-table"]//a/ @href').extract()

        return [Request(url=urljoin(response.url, category), callback=self.paginate) for category in category_links]

    def paginate(self, response):
        """Walks paginated index of businesses, creating requests to extract them"""

        #list of url strings for business pages to extract items from
        business_links = response.xpath('//td[@class="results_td_address"]//a/ @href').extract()
        business_requests = [Request(url=urljoin('http://businessdirectory.bizjournals.com/', business_link),
                                     callback=self.extract) for business_link in business_links]

        #url string for the last page, of format <category_name>/page/<int>
        last_page_link = response.xpath('//div[@class="last"]/a/ @href').extract()
        last_page = int(last_page_link[0].rsplit('/', 1)[1])

        current_resource = response.url.rsplit('/', 1)[-1]
        try:
            next_page = int(current_resource)+1
        except Exception:
            #Not an int so must be on page 1
            next_page = 2

        #Guessing that we can grab the remaining category pages using the <category>/page/<int> pattern
        page_requests = []

        for page in range(next_page, last_page+1):
            page_requests.append(Request(url='http://businessdirectory.bizjournals.com/'+
                                             urljoin(last_page_link[0], str(page)), callback=self.paginate))

        return page_requests+business_requests

    def extract(self, response):
        """Extracts data from a business page"""

        #Assume url pattern is /<city>/<category>/<duid>/<name>.html
        split_url = response.url.split('/')

        l = ItemLoader(item=BusinessItem(), response=response)
        l.add_xpath('name', "//div[@id='b2sec-alpha']/h2/text()")
        l.add_xpath("website", "//div[@class='b2secDetails-URL']//a/ @href")
        l.add_xpath("address1", "//div[@id='b2sec-alpha']/p[@class='b2sec-alphaText'][1]/ text()", MapCompose(unicode.strip))
        l.add_xpath("city", "//div[@id='b2sec-alpha']/p[@class='b2sec-alphaText'][2]/span[1]/ text()")
        l.add_xpath("state", "//div[@id='b2sec-alpha']/p[@class='b2sec-alphaText'][2]/span[2]/ text()")
        l.add_xpath("zip", "//div[@id='b2sec-alpha']/p[@class='b2sec-alphaText'][2]/span[3]/ text()")
        l.add_xpath("phone", "//div[@class='b2Local-greenTextmed']/ text()", MapCompose(unicode.strip))
        l.add_xpath("description", "//div[@id='b2sec-alpha']/p[4]/ text()")
        l.add_value("data_uid", split_url[-2])
        l.add_value("category", split_url[-3])
        l.add_value("data_source_url", response.url)

        return l.load_item()
