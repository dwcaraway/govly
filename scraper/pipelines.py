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
	        b.name=item['name']
	        b.phone=item['phone']
	        b.website=item['website']
	        b.facebook=item['facebook']
	        b.twitter=item['twitter']
	        b.logo=item['logo']
	        b.category=item['category']
	        b.description=item['description']
	        b.address1=item['address1']
	        b.address2=item['address2']
	        b.city=item['city']
	        b.state=item['state']
	        b.zip=item['zip']

	        db.session.add(b)
	        db.session.commit()

        return item