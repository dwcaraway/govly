from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import make_searchable
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from datetime import datetime
import json
# Define the database functions
db = SQLAlchemy()

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

class Person(db.Model):

    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    birthDate = db.Column(db.Date)
    givenName = db.Column(db.String)
    familyName = db.Column(db.String)
    telephone = db.Column(db.String)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

db.Table('employment', db.Model.metadata,
                db.Column('employer_id', None, db.ForeignKey('organizations.id')),
                db.Column('employee_id', None, db.ForeignKey('people.id'))
)

class Event(db.Model):
    __tablename__='events'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80))
    title = db.Column(db.String(120))
    description = db.Column(db.String(800))
    location = db.Column(db.String(250))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    source_id = db.Column(db.Integer, db.ForeignKey('organization_sources.id'))

    address1 = db.Column(db.String(300))
    address2 = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(70))
    zip = db.Column(db.String(15))
    latitude = db.Column(db.Float)
    longitude =db.Column(db.Float)
    projection = db.Column(db.String(15))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, url=None, title=None, location=None, start=None, description=None, end=None):
        self.url = url
        self.title = title
        self.description = description
        self.location = location
        self.start = start
        self.end = end

    def __repr__(self):
        return get_string_repr(self)

class OrganizationSource(db.Model):
    __tablename__='organization_sources'
    id = db.Column(db.Integer, primary_key=True)
    data_uid = db.Column(db.String)
    data_url = db.Column(db.String, nullable=False)
    spider_name = db.Column(db.String, nullable=False)
    organization_id= db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

    def __repr__(self):
        return get_string_repr(self)

class OrganizationQuery(BaseQuery, SearchQueryMixin):
    pass

class Organization(db.Model):
    """A data model for a business"""
    query_class = OrganizationQuery
    __tablename__='organizations'

    id = db.Column(db.Integer, primary_key=True)
    duns = db.Column(db.String)
    legalName = db.Column(db.String, nullable=False)
    logo = db.Column(db.String)
    naics = db.Column(db.String)
    cage = db.Column(db.String)
    taxID = db.Column(db.String)
    description = db.Column(db.String)

    addressCountry = db.Column(db.String)
    addressLocality = db.Column(db.String)
    addressRegion = db.Column(db.String)
    postalCode = db.Column(db.String)
    streetAddress = db.Column(db.String)
    lat = db.Column(db.String)
    lon = db.Column(db.String)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    employees = db.relationship("Person", secondary="employment", backref="employers")
    contacts = db.relationship("ContactPoint", backref="organization")
    keywords = db.relationship("OrganizationKeyword", backref="organization")
    sources = db.relationship("OrganizationSource", backref="organization")

    search_vector = db.Column(TSVectorType('legalName', 'description'))

    def __repr__(self):
        return get_string_repr(self)

class OrganizationKeyword(db.Model):
    __tablename__= 'organization_keywords'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    keyword = db.Column(db.String, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return get_string_repr(self)

class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    rel = db.Column(db.String, nullable=False)
    href = db.Column(db.String, nullable=False)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class ContactPoint(db.Model):
    __tablename__= 'contact_points'

    id = db.Column(db.Integer, primary_key=True)
    #operating_hours = db.relationship("OperatingHours", backref="contact")
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    telephone = db.Column(db.String)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)

# class OperatingHours(db.Model):
#     __tablename__= 'operating_hours'
#     id = db.Column(db.Integer, primary_key=True)
#     closes = db.Column(db.String)
#     opens = db.Column(db.String)
#     dayOfWeek = db.Column(db.String)
#     contact_id = db.Column(db.Integer, db.ForeignKey('contact_points.id'))

#enable full-text search of postgres
make_searchable()
