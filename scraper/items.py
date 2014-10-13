#  Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BusinessItem(Item):
    name = Field()
    website = Field()
    logo = Field()
    address_single_entry = Field() #An address in a single text field instead of parsed out
    address1 = Field()
    address2 = Field()
    city = Field()
    state = Field()
    zip = Field()
    phone = Field()
    email = Field()
    description = Field()
    facebook = Field()
    twitter = Field()
    linkedin = Field()
    category = Field()
    data_source_url = Field()
    data_uid = Field()
