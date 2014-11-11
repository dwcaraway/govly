from app.model import db, Organization, OrganizationSource, ContactPoint
from app import create_application
from app.config import DevelopmentConfig
from scrapy import log
import phonenumbers
import string
from address import AddressParser

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class PhoneNormalizationPipeline:
    """Normalizes a telephone"""

    def process_item(self, item, spider):
        p_original = item.get('telephone')

        #Normalize telephone numbers to INTERNATIONAL format, assumes US telephone number to dial from
        try:
            p = phonenumbers.parse(p_original, 'US')
            p = phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            item['telephone'] = p
        except IndexError:
            item['telephone'] = None
            log.msg("telephone number not found at url: %s" % item['data_source_url'], level=log.DEBUG)
        except Exception:
            item['telephone'] = None
            log.msg("Unable to parse telephone: %s" % p_original, level=log.DEBUG)
        return item

class AddressNormalizationPipeline:
    """
    Normalizes and combines the addresses.

    First, we combine all the street address parts e.g. ['134 some st.', 'apt. #302'] becomes '134 some st., apt. #302'
    """
    def process_item(self, item, spider):
        address = item.get('streetAddress')

        if address:
            item['streetAddress'] = string.join(address, ', ')

        return item

# class CreateSourcePipeline:
#     def __init__(self, app=None):
#         if app is None:
#             self.app = create_application()
#         else:
#             self.app = app
#
#     def process_item(self, item , spider):
#         #TODO source lookup in BusinessItemLoader (once) and cache
#         #assumes that note more than one source per spider which is fine
#         business
#         if item.get('source_id'):
#             return item
#
#         with self.app.app_context():
#             s = OrganizationSource.query.filter_by(name=spider.name).first()
#             if s is None:
#                 log.msg("Source %s not found. Creating it." % spider.name, level=log.DEBUG)
#                 s = OrganizationSource(name = spider.name)
#                 db.session.add(s)
#                 db.session.commit()
#
#             item['source_id'] = s.id
#
#         return item


class DatabasePipeline:
    """Sends processed items to storage"""

    def __init__(self, app=None):
        if app is None:
            self.app = create_application()
        else:
            self.app = app

        with self.app.app_context():
            db.create_all()

    def process_item(self, item, spider):
        organization = None

        with self.app.app_context():
            if item.get('data_uid'):
                os = OrganizationSource.query.filter_by(data_uid=item['data_uid'], spider_name=spider.name).first()

                if os is not None:
                    organization = os.organization

            if organization is None and item.get('telephone'):
                #Try to get by telephone, assumes telephone normalized to INTERNATIONAL standard
                c = ContactPoint.query.filter_by(telephone=item['telephone']).first()
                if c is not None:
                    organization = c.organization

            if organization is None:
                log.msg('business not found, creating new one', level=log.DEBUG)
                organization = Organization(legalName=item['legalName'])
                db.session.add(organization)

            if organization.contacts is None and (item.get('telephone') or item.get('email')):
                c = ContactPoint(name='main', telephone=item.get('telephone'), email=item.get('email'))
                c.organization = organization
                db.session.add(c)

                os = OrganizationSource(data_uid=item.get('data_uid'), data_url=item['source_url'], spider_name=spider.name, organization_id=organization.id)
                db.session.add(os)

            # for key, value in item.iteritems():
            #     setattr(organization, key, value)
            organization.streetAddress = item.get('streetAddress')
            organization.addressLocality = item.get('addressLocality')
            organization.addressRegion = item.get('addressRegion')
            organization.postalCode = item.get('postalCode')
            organization.description = item.get('description')

            db.session.commit()

        return item