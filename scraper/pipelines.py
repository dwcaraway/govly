from app.model import db, Business
from app import create_application
from app.config import DevelopmentConfig

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

    def process_item(self, item, spider):

    	with self.app.app_context():
	        b = Business()
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