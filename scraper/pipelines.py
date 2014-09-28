from app.model import db
from app import create_application
from app.config import DevelopmentConfig

app = create_application(DevelopmentConfig)


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class DaytonLocalPipeline(object):
    """Dayton business processing"""
    def process_item(self, item, spider):
        return item

class DatabaseOutputPipeline():
    """Sends processed items to storage"""

    def process_item(self, item, spider):
        with app():
            #Save database stuff
            

        return item