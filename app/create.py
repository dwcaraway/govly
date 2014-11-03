from app.new_model import metadata
from sqlalchemy import create_engine

engine = create_engine('postgresql://vitals:vitals@localhost:5432/vitals')
metadata.create_all(engine)
