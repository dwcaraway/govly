__author__ = 'dwcaraway'

from scrapy.spider import Spider
from scrapy.http import FormRequest
from scraper.items import BusinessItem

class DaytonChamberSpider(Spider):
    name = "dayton_chamber"
    allowed_domains = ["daytonchamber.org"]
    start_urls = [
        "http://www.daytonchamber.org/index.cfm/mb/find-a-member1/"
    ]

    def parse(self, response):
        yield FormRequest.from_response(response,
                                        formname='searchForm',
                                        formdata={},
                                        callback=self.extract)

    def extract(self, response):
        """
        Takes the data out of the members entries
        """
        items = []

        containers = response.xpath('//div[@id="membersearchresults"]//div[@id="container"]')

        for container in containers:

            item = BusinessItem()

            item['data_source_url'] = response.url

            rows = container.css('div.row')

            row_dict = {}

            # from scrapy.shell import inspect_response
            # inspect_response(response, self)

            for row in rows:
                key = row.css('div.leftcol').xpath('./text()').extract()

                if len(key) == 0:
                    # No key, so don't bother looking for a value
                    continue

                key = key[0].strip()

                if key == 'Business Name:':
                    value = row.css('div.rightcol').xpath('./strong/text()').extract()
                elif key == 'Website:':
                    value = row.css('div.rightcol').xpath('./a/ @href').extract()
                else:
                    value = row.css('div.rightcol').xpath('./text()').extract()

                if len(value) == 0:
                    #No value, so don't bother storing
                    continue

                value = value[0].strip()

                #Finally store the results in the dict
                row_dict[key] = value


            item['name'] = row_dict.get('Business Name:', None)
            item['category'] = row_dict.get('Business Category:', None)
            item['raw_address']= row_dict.get('Address:', None)
            item['website'] = row_dict.get('Website:', None)
            item['telephone'] = row_dict.get('Phone Number:', None)

            items.append(item)

        return items

if __name__ == '__main__':
    from scrapy.http import Request
    from scrapy.http.response.xml import XmlResponse


    with open('./chamber_example.html', 'r') as f:
        request = Request(url='http://localhost')
        response = XmlResponse(url='http://localhost', request=request, body=f.read(), encoding='utf-8')

    print DaytonChamberSpider.extract(DaytonChamberSpider(), response=response)
