from app.model import db, Business, Source
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

        #Normalize phone numbers
        try:
            p = phonenumbers.parse(p_original, 'US')
            p = phonenumbers.normalize_digits_only(p)
            item['phone'] = p
        except IndexError:
            item['phone'] = None
            log.msg("phone number not found at url: %s" % item['data_source_url'], level=log.DEBUG)
        except Exception:
            item['phone'] = None
            log.msg("Unable to parse phone: %s" % p_original, level=log.DEBUG)
        return item

class CreateSourcePipeline:
    def __init__(self, app=None):
        if app is None:
            self.app = create_application()
        else:
            self.app = app

    def process_item(self, item , spider):
        #TODO source lookup in BusinessItemLoader (once) and cache
        #assumes that note more than one source per spider which is fine
        if item.get('source_id'):
            return item

        with self.app.app_context():
            s = Source.query.filter_by(name=spider.name).first()
            if s is None:
                log.msg("Source %s not found. Creating it." % spider.name, level=log.DEBUG)
                s = Source(name = spider.name)
                db.session.add(s)
                db.session.commit()

            item['source_id'] = s.id

        return item


class DatabasePipeline:
    """Sends processed items to storage"""

    def __init__(self, app=None):
        if app is None:
            self.app = create_application()
        else:
            self.app = app

    def process_item(self, item, spider):
        with self.app.app_context():
            b = Business.query.filter_by(source_data_id=item.get('source_data_id', '-1'), source_id=item['source_id']).first()

            if b is None and item.get('phone'):
                #Try to get by phone
                b = Business.query.filter_by(phone=item['phone'], source_id=item['source_id']).first()

            if b is None:
                log.msg('business not found, creating new one', level=log.DEBUG)
                b = Business()
                db.session.add(b)
                # b.source
                # b.source_data_id = item.get('source_data_id')

            for key, value in item.iteritems():
                setattr(b, key, value)

            db.session.commit()

        return item