# Example of usage composite foreign keys in SQL Alchemy

import sqlalchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Index, Sequence # Seq - required for Oracle
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Base type of all tables/models
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# DEFINE MODEL

# Codes -> Data
# ONE -> MANY

class Codes(Base):
    __tablename__ = "codes"
    __table_args__ = (
        UniqueConstraint('list', 'code', name='idx_code'),
        )

    # PK
    id = Column(Integer, Sequence('codes_id_seq', start=100), primary_key=True)

    # Unique composite key
    code = Column(Integer, nullable=False)
    list = Column(Integer, nullable=False)

    def __repr__(self):
        return "<User(id: %r, code: %r, list: %r)>" % (self.id, self.code, self.list)

class Data(Base):
    __tablename__ = "data"
    __table_args__ = (
        ForeignKeyConstraint(['list_id', 'code_id'], ['codes.list', 'codes.code']),
        Index('idx_code', 'list_id', 'code_id', unique=True)
        )

    # PK
    id = Column(Integer, Sequence('data_id_seq', start=100), primary_key=True)

    # Foreign composite key
    code_id = Column(Integer, nullable=False)
    list_id = Column(Integer, nullable=False)

    code = relationship("Codes")


# TESTING
print(sqlalchemy.__version__ )

# Connect to sqlite db engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

# Create tables
Base.metadata.create_all(engine)

# Create session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

# ADD CODE LISTS
c1 = Codes(code=1, list=1)
c2 = Codes(code=2, list=1)

session = Session()
session.add(c1)
session.add(c2)

session.add_all([Codes(code=1, list=2), Codes(code=2, list=2)])

session.commit()
session.close()

# ADD DATA
print("adding data")

d1 = Data(code_id=1, list_id=1)
session = Session()
session.add_all([d1])
session.commit() # d1.code now contains object

c3 = Codes(code=3, list=1)
session.add(c3)
session.commit()

d2 = Data(code=c3)
session.add(d2) # d2.code now contains object
session.commit()

print("done")





