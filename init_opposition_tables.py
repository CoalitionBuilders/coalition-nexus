from sqlalchemy import create_engine
from models.opposition import Base

# Create tables
engine = create_engine('sqlite:///coalition.db')
Base.metadata.create_all(engine)

print('Opposition tables created.')