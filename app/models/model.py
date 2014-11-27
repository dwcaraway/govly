from datetime import datetime
from flask.ext.security import UserMixin, RoleMixin

import json
# Define the database functions

from ..framework.sql import (
    db,
    Model
)

def get_string_repr(obj):
    #Using str for value since datetime is not json serializable
    new_obj = {}
    for key, value in obj.__dict__.iteritems():
        if not key.startswith('_') and value:
            if type(value) is datetime:
                new_obj[key] = str(value)
            else:
                new_obj[key] = value

    return json.dumps(new_obj)

class Person(Model):

    __tablename__ = 'people'

    birthDate = db.Column(db.Date)
    givenName = db.Column(db.String(255))
    familyName = db.Column(db.String(255))
    telephone = db.Column(db.String(50))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

db.Table('employment', Model.metadata,
                db.Column('employer_id', None, db.ForeignKey('organizations.id')),
                db.Column('employee_id', None, db.ForeignKey('people.id'))
)

class OrganizationSource(Model):
    __tablename__='organization_sources'
   
    data_uid = db.Column(db.String(40))
    data_url = db.Column(db.String(100), nullable=False)
    spider_name = db.Column(db.String(50), nullable=False)
    organization_id= db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

    def __repr__(self):
        return get_string_repr(self)

class OrganizationRecord(Model):
    __tablename__='organization_records'
   
    record = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    organization_id= db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

    def __repr__(self):
        return get_string_repr(self)

class Organization(Model):
    """A data model for a business"""

    __tablename__='organizations'

    duns = db.Column(db.String(9))
    dunsPlus4 = db.Column(db.String(4))
    legalName = db.Column(db.String(50), nullable=False)
    logo = db.Column(db.String(200))
    naics = db.Column(db.String(6))
    cage = db.Column(db.String(5))
    taxID = db.Column(db.String(9))
    description = db.Column(db.String(1000))

    countryCode = db.Column(db.String(2))#ISO 3166-1 country code
    addressLocality = db.Column(db.String(100))
    addressRegion = db.Column(db.String(100))
    postalCode = db.Column(db.String(25))
    streetAddress = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    employees = db.relationship("Person", secondary="employment", backref="employers")
    contacts = db.relationship("ContactPoint", backref="organization")
    keywords = db.relationship("OrganizationKeyword", backref="organization")
    sources = db.relationship("OrganizationSource", backref="organization")
    links = db.relationship("Link", backref="organization")
    records = db.relationship("OrganizationRecord", backref="organization")

    def __repr__(self):
        return get_string_repr(self)

class OrganizationKeyword(Model):
    __tablename__= 'organization_keywords'
   
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    keyword = db.Column(db.String(40), nullable=False)

class Link(Model):
    __tablename__ = 'links'

   
    rel = db.Column(db.String(20), nullable=False)
    href = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Product(Model):
    __tablename__ = 'products'

   
    name = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(150))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class ContactPoint(Model):
    __tablename__= 'contact_points'

    operating_hours = db.relationship("OperatingHours", backref="contact")
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)

class OperatingHours(Model):
    __tablename__= 'operating_hours'

    closes = db.Column(db.Time)
    opens = db.Column(db.Time)
    dayOfWeek = db.Column(db.String(3))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact_points.id'), nullable=False)

def enable_full_text_search():
    """
    Add full-text search capabilities to the database models. This must be called prior to
    any database model creation or migration
    """
    from flask.ext.sqlalchemy import BaseQuery
    from sqlalchemy_searchable import SearchQueryMixin

    class OrganizationQuery(BaseQuery, SearchQueryMixin):
        pass

    from sqlalchemy_searchable import make_searchable

    from sqlalchemy_utils.types import TSVectorType

    #Update the models query_class if full-text search desired
    Organization.query_class = OrganizationQuery
    search_vector = db.Column(TSVectorType('legalName', 'description'))

    #enable full-text search of postgres. call after models are augmented.
    make_searchable()
