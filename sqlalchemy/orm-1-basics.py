# The declarative system is normally used to configure object relational mapping.

# Creates type Base, it is registry for set of classes (metadata) that descent from Base
# Usually it is enough to have one Base for all types, but it is no problem to work with multiple Bases
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Base is type created by function (we could create multiple Bases)
print(Base) # <class 'sqlalchemy.ext.declarative.api.Base'>

# Base holds metadata of derived types
print(Base.metadata)


# Basic mapping
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<User(id: %r, name: %r)>" % (self.id, self.name)

# declarative system creates Table metadata with columns that is associated with type
print(repr(User.__table__))

# mapper object mediates the relationship between User object and "user" Table object
print(repr(User.__mapper__))

# Creating data
# Derived type from Base has default constructor, accepting field names as arguments
u1 = User(name="slavo")
u2 = User(name="peter")

print(u1)       # <User('slavo')>
print(u2.id)    # None, id is primary key that is initiated with None

# talking to the database
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)

# ORM created metadata for all derived types from Base
Base.metadata.create_all(engine)

# To presist and load domain objects from database we use a Session object
# Session is bounded to the engine and knows how to use it
# you can have multiple sessions for various use cases 
# (for example with enabled transactions or without for e.g. logging or fast reads)
# by default Session is configured with *Automatic transactions* and *auto invalidation of data*.
# This means session assumes it knows nothing about data until it is in a transaction. When transaction starts
# it reloads data from database
from sqlalchemy.orm import Session
session = Session(bind=engine)

# adding new object to the session (not yet the db - justing in *pending* state)
# session uses IdentityMap pattern to store objects in-memory and keeps track of them
session.add(u1)
session.add(u2)

# list of objects added to the session can be seen using *new* property
# in pending state, not yet flushed to the database
print(session.new)

# session with *flush* *pending* objects in memory to the database before each Query
# it is also called auto-flush, it is possible to turn it off
s = session.query(User).filter_by(name="slavo").first();
print(s)

# Session maintains a *unique* object per identity so "s" and "u1" are same objects (in memory via identity map)
print(s is u1) # True

