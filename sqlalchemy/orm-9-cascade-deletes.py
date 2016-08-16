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

# Many-to-One relationship (Adr->User - one user can live on multiple addresses)
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

u1.addresses = [
    Address(email="matus@matus.com"),
    Address(email="matus@woho.com"),
    Address(email="matus@microsoft.io")
]

session.add(u1) # also added addresses
session.commit()

# ---------------
# Cascade deletes
# ---------------

matus = session.query(User).filter_by(name="Matus").one()
del matus.addresses[0] # sets user_id of address to NULL
session.commit()

# removing an Address sets its foreign key to NULL
# we would prefer it gets deleted

# This can be configured on relationship() using "delete-orphan" cascade
# on the User->Address relationship.
User.addresses.property.cascade = "all, delete, delete-orphan"

matus = session.query(User).filter_by(name="Matus").one()
del matus.addresses[0] # sets user_id of address to NULL
session.commit()

# deleting the User will also delete all Address objects
session.delete(matus)
session.commit()

# if database supports and configured on-delete-cascade on foreign key the db can take care of deleting
# children. This is more efficient than above approach because sqlalchemy has to load data first
# and delete them one by one. You can tell sqlalchemy that a relationship has on-delete-cascade configured
# on db level so db will do deletes automatically - this is more efficient.
