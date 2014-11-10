import sys
sys.path.append('../')

#Ensure that the database has been created!
from app import create_application
from app.model import db

app = create_application()
with app.app_context():
    db.create_all()