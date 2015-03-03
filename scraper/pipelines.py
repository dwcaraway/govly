# from sqlalchemy import or_
from scrapy import log
import phonenumbers

# from app.models.model import Organization, OrganizationSource, ContactPoint, OrganizationKeyword, Link, OrganizationRecord
# from app.framework.sql import db
# from app import create_app


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
            log.msg("telephone number not found at url: %s" % item['data_url'], level=log.DEBUG)
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

        if address and not isinstance(address, basestring):
            item['streetAddress'] = ', '.join(address)

        return item

# class DatabasePipeline:
#     """
#     Sends processed items to storage
#
#     We do try to avoid duplicate entries (especially from the same source).
#     """
#
#     DBSession = None
#
#     def __init__(self, app=None):
#         if app is None:
#             self.app = create_app()
#         else:
#             self.app = app
#
#         with self.app.app_context():
#             db.create_all()
#
#             from sqlalchemy.orm import scoped_session, sessionmaker
#             self.DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db.engine))
#
#     def process_item(self, item, spider):
#         organization = None
#
#         with self.app.app_context():
#             if item.get('data_uid'):
#                 organization = Organization.query.join(OrganizationSource).filter(OrganizationSource.data_uid==item.get('data_uid')).\
#                     filter(OrganizationSource.spider_name==spider.name).first()
#
#             if organization is None:
#                 organization = Organization.query.filter_by(legalName=item['legalName']).join(OrganizationSource).filter(OrganizationSource.data_url==item['data_url']).first()
#
#             if organization is None and item.get('telephone'):
#                 #Try to get by telephone, assumes telephone normalized to INTERNATIONAL standard
#                 c = ContactPoint.query.filter_by(telephone=item['telephone']).first()
#                 if c:
#                     organization = c.organization
#
#             if organization is None:
#                 log.msg('business not found, creating new one', level=log.DEBUG)
#                 organization = Organization(legalName=item['legalName'])
#                 db.session.add(organization)
#
#                 OrganizationSource(data_uid=item.get('data_uid'), data_url=item.get('data_url'), spider_name=spider.name, organization=organization)
#
#             if item.get('telephone') or item.get('email'):
#                 c = None
#
#                 if not item.get('email'):
#                     c = ContactPoint.query.filter_by(telephone=item['telephone']).first()
#                 elif not item.get('telephone'):
#                     c = ContactPoint.query.filter_by(email=item['email']).first()
#                 else:
#                     c = ContactPoint.query.filter(or_(ContactPoint.telephone == item.get('telephone'), ContactPoint.email == item.get('email'))).first()
#                 if c:
#                     if item.get('telephone'):
#                         c.telephone = item.get('telephone')
#                     if item.get('email'):
#                         c.email = item.get('email')
#                 else:
#                     c = ContactPoint(name='main', telephone=item.get('telephone'), email=item.get('email'), organization=organization)
#
#             for x in ['website', 'facebook', 'linkedin', 'twitter']:
#                 if item.get(x):
#                     found = False
#                     for link in organization.links:
#                         if link.rel == x:
#                             link.href = item.get(x)
#                             found = True
#                             break
#                     if not found:
#                         Link(rel=x, href=item.get(x), organization=organization)
#
#             if item.get('category'):
#                 existing_categories = [k.keyword for k in organization.keywords]
#                 if item['category'] not in existing_categories:
#                     OrganizationKeyword(keyword=item['category'], organization=organization)
#
#             if item.get('record'):
#                 found = False
#                 for r in organization.records:
#                     if r.type == item['record_type']:
#                         r.record = item['record']
#                         found = True
#                 if not found:
#                     OrganizationRecord(record=item['record'], type=item['record_type'], organization=organization)
#
#             for key, value in item.iteritems():
#                 setattr(organization, key, value)
#
#             db.session.commit()
#
#         return item