from app.model import db, Organization, OrganizationSource, ContactPoint
from app import create_application
from app.config import DevelopmentConfig
from scrapy import log
import phonenumbers
from address import AddressParser

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class PhoneNormalizationPipeline:
    """Normalizes a phone"""

    def process_item(self, item, spider):
        p_original = item.get('phone')

        #Normalize phone numbers to INTERNATIONAL format, assumes US phone number to dial from
        try:
            p = phonenumbers.parse(p_original, 'US')
            p = phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            item['phone'] = p
        except IndexError:
            item['phone'] = None
            log.msg("phone number not found at url: %s" % item['data_source_url'], level=log.DEBUG)
        except Exception:
            item['phone'] = None
            log.msg("Unable to parse phone: %s" % p_original, level=log.DEBUG)
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
        with app.app_context():
            db.create_all()

    def process_item(self, item, spider):
        b = None

        with self.app.app_context():
            if item.get('data_uid'):
                o = OrganizationSource.query.filter_by(data_uid=item['data_uid'], spider_name=spider.name).first()
                if o is not None:
                    b = o.organization

            if b is None and item.get('phone'):
                #Try to get by phone, assumes phone normalized to INTERNATIONAL standard
                c = ContactPoint.query.filter_by(telephone=item['phone']).first()
                if c is not None:
                    b = c.organization

            if b is None:
                log.msg('business not found, creating new one', level=log.DEBUG)
                b = Organization()
                db.session.add(b)

            for key, value in item.iteritems():
                setattr(b, key, value)

            db.session.commit()

        return item