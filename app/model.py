from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from datetime import datetime
import json
# Define the database functions
db = SQLAlchemy()

#enable full-text search of postgres
make_searchable()

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


class Organization(db.Model):

    __tablename__= 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    duns = db.Column(db.String)
    legalName = db.Column(db.String)
    logo = db.Column(db.String)
    naics = db.Column(db.String)
    cage = db.Column(db.String)
    taxID = db.Column(db.String)
    description = db.Column(db.Text)

    addressCountry = db.Column(db.String)
    addressLocality = db.Column(db.String)
    addressRegion = db.Column(db.String)
    postOfficeBoxNumber = db.Column(db.String)
    postalCode = db.Column(db.String)
    streetAddress = db.Column(db.String)
    lat = db.Column(db.String)
    lon = db.Column(db.String)

    source_id = db.Column(db.Integer, db.ForeignKey('organization_sources.id'))

    search_vector = db.Column(TSVectorType('name', 'description'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    employees = db.relationship("Person", secondary="employment", backref="employers")

db.Table('employment', db.Model.metadata,
                db.Column('employer_id', None, db.ForeignKey('organizations.id')),
                db.Column('employee_id', None, db.ForeignKey('people.id'))
)

class Event(db.Model):
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
    source_unique_id = db.Column(db.String)
    source_data_url = db.Column(db.String)
    spider_name = db.Column(db.String)

    organization = db.relationship("Organization", backref="sources")

    def __repr__(self):
        return get_string_repr(self)

class Business(db.Model):
    """A data model for a business"""

    id = db.Column(db.Integer, primary_key=True)
    duns = db.Column(db.String)
    legalName = db.Column(db.String)
    logo = db.Column(db.String)
    naics = db.Column(db.String)
    cage = db.Column(db.String)
    taxID = db.Column(db.String)

    name = db.Column(db.String)
    phone = db.Column(db.String)
    logo = db.Column(db.String)
    category = db.Column(db.String)
    description = db.Column(db.String)

    raw_address = db.Column(db.String)
    address1 = db.Column(db.String)
    address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude =db.Column(db.Float)

    source_data_id = db.Column(db.String(15))
    source_data_url = db.Column(db.String(400))
    source_id = db.Column(db.Integer, db.ForeignKey('organization_sources.id'))

    search_vector = db.Column(TSVectorType('name', 'category', 'description'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name=None, phone=None):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return get_string_repr(self)

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
    rel = db.Column(db.String)
    href = db.Column(db.String)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class ContactPoint(db.Model):
    __tablename__= 'contact_points'

    id = db.Column(db.Integer, primary_key=True)
    operating_hours = db.relationship("OperatingHours", backref="contact")
    email = db.Column(db.String)
    faxNumber = db.Column(db.String)
    telephone = db.Column(db.String)

class OperatingHours(db.Model):
    __tablename__= 'operating_hours'
    id = db.Column(db.Integer, primary_key=True)
    closes = db.Column(db.String)
    opens = db.Column(db.String)
    dayOfWeek = db.Column(db.String)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact_points.id'))
