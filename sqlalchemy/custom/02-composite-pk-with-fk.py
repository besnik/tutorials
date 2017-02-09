# Example of usage composite primary key in combination with FK in SQL Alchemy

import sqlalchemy
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy import Index, Sequence # Seq - required for Oracle
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Base type of all tables/models
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# DEFINE MODEL

# Codes -> Data
# ONE -> MANY

class Codelist(Base):
    __tablename__ = "CODELISTS"
    
    # PK
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<Codelist(id: %r)>" % (self.id)

class Code(Base):
    __tablename__ = "CODES"
    __table_args__ = (
        PrimaryKeyConstraint('list', 'code', name='codes_pk'),
        UniqueConstraint('list', 'value', name='idx_codes_lv'),
        )

    # PK
    code = Column(Integer)
    list = Column(Integer)

    # Value
    value = Column(String, nullable=False)

    def __repr__(self):
        return "<Code(code: %r, list: %r, value: %r)>" % (self.code, self.list, self.value)

class Data(Base):
    __tablename__ = "DATA"
    __table_args__ = (
        ForeignKeyConstraint(['list_id', 'code_id'], ['CODES.list', 'CODES.code']),
        Index('idx_data_code', 'list_id', 'code_id')
        )

    # PK
    id = Column(Integer, Sequence('data_id_seq', start=101), primary_key=True)

    # Foreign composite key
    code_id = Column(Integer, nullable=False)
    list_id = Column(Integer, nullable=False)

    code = relationship("Code")


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
c1 = Code(code=1, list=1, value="ico")
c2 = Code(code=2, list=1, value="dic")

session = Session()
session.add(c1)
session.add(c2)

session.add_all([Code(code=1, list=2, value="sk"), Code(code=2, list=2, value="de")])

session.commit()
session.close()

# ADD DATA
print("adding data")

d1 = Data(code_id=1, list_id=1)
session = Session()
session.add_all([d1])
session.commit() # d1.code now contains object

c3 = Code(code=3, list=1, value="nico")
session.add(c3)
session.commit()

d2 = Data(code=c3)
session.add(d2) # d2.code now contains object
session.commit()

print("done")





