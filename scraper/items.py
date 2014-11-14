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
    streetAddress = Field()
    addressLocality = Field()
    addressRegion = Field()
    postalCode = Field()
    latitude = Field()
    longitude = Field()
    telephone = Field()
    email = Field()
    description = Field()
    facebook = Field()
    twitter = Field()
    linkedin = Field()
    category = Field()
    data_url = Field()
    data_uid = Field()

    duns = Field()
    dunsPlus4 = Field()
    naics = Field()
    cage = Field()

    record = Field() #Bulk record of additional data
    record_type = Field() #Bulk record type e.g. 'SAM' or 'SAM_EXCLUSION'
