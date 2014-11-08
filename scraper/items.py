#  Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BusinessItem(Item):
    legalName = Field()
    website = Field()

    image_urls = Field()
    images = Field()

    raw_address = Field() #An address in a single text field instead of parsed out
    address1 = Field()
    address2 = Field()
    city = Field()
    state = Field()
    zip = Field()
    latitude = Field()
    longitude = Field()
    phone = Field()
    email = Field()
    description = Field()
    facebook = Field()
    twitter = Field()
    linkedin = Field()
    category = Field()
    source_url = Field()
    source_data_id = Field()

    source_id = Field()
