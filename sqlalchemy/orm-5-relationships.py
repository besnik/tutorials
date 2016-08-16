from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Base
Base = declarative_base() 

# Concrete type
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<User(id: %r, name: %r)>" % (self.id, self.name)

# Engine and create tables
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

# Session with identity map
from sqlalchemy.orm import Session
session = Session(bind=engine)

# adding multiple objects as *pending*
u1 = User(name="slavo")
session.add_all([
    u1,
    User(name="jano"),
    User(name="vlado"),
    User(name="peter"),
    User(name="brano")
])

# finalize transaction
session.commit();

#-------------------------------------------------------------------------------
# Many-to-One relationship (Adr->User - one user can live on multiple addresses)
#-------------------------------------------------------------------------------
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# in sqlalchemy we have to declare relation ship twice
# 1) relation type at core level
# 2) relationship on orm level and object level
class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", backref="addresses") # creates addresses property on referenced object

    def __repr__(self):
        return "<Address(%r)>" % self.email

# Creates addresses table
Base.metadata.create_all(engine)

u1 = User(name="Matus")
print(u1)               # <User(id: None, name: 'Matus')>
print(u1.addresses)     # []

u1.addresses = [
    Address(email="matus@matus.com"),
    Address(email="matus@woho.com"),
    Address(email="matus@microsoft.io")
]

# everything is in-memory now
print(u1)
print(u1.addresses[1])
print(u1.addresses[1].user)

# Cascading objects when adding into session
session.add(u1) # also added addresses
print(session.new)

# write changes to db, ends transaction, data are expired
session.commit()

# after expiration, user.addresses emits *lazy loading* when first accessed
print(u1)
print(u1.addresses) # now collection is in-memory until transaction ends

print(u1.addresses) # won't hit database as data are already in memory


# collections and references are updated by manipulating objects, not primary/foreign keys
v = session.query(User).filter(User.name == "vlado").one();
u1.addresses[1].user = v; # user vlado now has one address, user u1 has two
session.commit()

print(u1.addresses)
print(v.addresses)