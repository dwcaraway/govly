from app.model import db, Business, Source
from app import create_application
from app.config import DevelopmentConfig
import logging

logger = logging.getLogger(__name__)

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class DatabasePipeline():
    """Sends processed items to storage"""

    def __init__(self, app=None):
        if app is None:
            self.app = create_application(DevelopmentConfig)
        else:
            self.app = app

        with app.app_context():
            logger.debug('Source Count: %d', len(Source.query.all()))
            s = Source.query.filter_by(name='daytonlocal.com').first()
            if s is None:
                logger.debug("Source daytonlocal.com not found. Creating it.")
                s = Source()
                s.name = 'daytonlocal.com'
                db.session.add(s)
                db.session.commit()

            self.sid = s.id


    def process_item(self, item, spider):

        with self.app.app_context():
            logger.debug('Business Count: %d, item_data_id=%s, sid=%d', len(Business.query.all()), item.get('data_uid', '-1'), self.sid)

            b = Business.query.filter_by(source_data_id=item.get('data_uid', '-1'), source_id=self.sid).first()
            if b is None:
                logger.debug('business not found, creating new one')
                b = Business()
                b.source_data_id = item.get('uid')
                b.source_data_url = item.get('data_source_url')

            b.name=item.get('name')
            b.phone=item.get('phone')
            b.website=item.get('website')
            b.facebook=item.get('facebook')
            b.twitter=item.get('twitter')
            b.logo=item.get('logo')
            b.category=item.get('category')
            b.description=item.get('description')
            b.address1=item.get('address1')
            b.address2=item.get('address2')
            b.city=item.get('city')
            b.state=item.get('state')
            b.zip=item.get('zip')

            db.session.add(b)
            db.session.commit()

        return item