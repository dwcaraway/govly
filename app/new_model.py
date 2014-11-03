from sqlalchemy import Table, Date, Column, Integer, String, MetaData, ForeignKey, Text

metadata = MetaData()

people = Table('people', metadata,
                Column('id', Integer, primary_key=True),
                Column('birthDate', Date),
                Column('givenName', String),
                Column('familyName', String),
                Column('telephone', String)
)

places = Table('places', metadata,
               Column('id', Integer, primary_key=True),
               Column('addressCountry', String),
               Column('addressLocality', String),
               Column('addressRegion', String),
               Column('postOfficeBoxNumber', String),
               Column('postalcode', String),
               Column('streetAddress', String),
               Column('lat', String),
               Column('lon', String)
               )


person_place = Table('person_place', metadata,
                Column('id', Integer, primary_key=True),
                Column('person_id', None, ForeignKey('people.id')),
                Column('place_id', None, ForeignKey('places.id')),
                Column('relation', String)
)

person_contact = Table('person_contact', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('person_id', None, ForeignKey('people.id')),
                       Column('contact_id', None, ForeignKey('contact_points.id')),
                       )

employment = Table('employment', metadata,
                Column('id', Integer, primary_key=True),
                Column('employer_id', None, ForeignKey('organizations.id')),
                Column('employee_id', None, ForeignKey('people.id'))
)

organization_place = Table('organization_place', metadata,
                Column('id', Integer, primary_key=True),
                Column('organization_id', None, ForeignKey('organizations.id')),
                Column('place_id', None, ForeignKey('places.id')),
                Column('relation', String)
                          )

organizations = Table('organizations', metadata,
                    Column('id', Integer, primary_key=True),
                   Column('duns', String),
                   Column('legalName', String),
                   Column('logo', String),
                   Column('naics', String),
                   Column('cage', String),
                   Column('taxID', String),
                   Column('description', Text),
)

organization_links = Table('organization_link', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('rel', Text),
                    Column('href', Text),
                    Column('organization_id', None, ForeignKey('organizations.id'))
                           )

organization_product = Table('organization_product', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('organization_id', None, ForeignKey('organizations.id')),
                    Column('product_id', None, ForeignKey('products.id'))
                             )

products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('url', String)
                 )

addresses = Table('email_addresses', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('person_id', None, ForeignKey('people.id')),
                  Column('email_address', String, nullable=False)
)

contacts = Table('contact_points', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('contactType', String),
                 Column('email', String),
                 Column('faxNumber', String),
                 Column('telephone', String)
                 )

contact_operating_hours = Table('contact_points_operating_hours', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('closes', String),
                  Column('opens', String),
                  Column('dayOf_Week', String),
Column('contact_point_id', None, ForeignKey('contact_points.id'))
                                )
contact_locations= Table('contact_points_places', metadata,
                  Column('id', Integer, primary_key=True),
Column('contact_point_id', None, ForeignKey('contact_points.id')),
Column('place_id', None, ForeignKey('places.id'))
                                )