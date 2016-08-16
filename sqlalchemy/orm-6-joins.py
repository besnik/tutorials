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

u2 = User(name="Martin")
u2.addresses = [Address(email="martin@martin.com")]

session.add(u1) # also added addresses
session.add(u2)
session.commit()

# -----------------------------------------------------------
# Joins
# -----------------------------------------------------------

# query can select from multiple tables at once. joins from left most entity
# example of *implicit join*

rows = session.query(User, Address).filter(User.id == Address.user_id).all();
for row in rows:
    print(row)

# *explicit join*
rows = session.query(User, Address).join(Address, User.id == Address.user_id).all();
for row in rows:
    print(row)

# *join using relationship()*
rows = session.query(User, Address).join(User.addresses).all()
for row in rows:
    print(row)

# automatical join if there is no ambiguity (e.g. one foreign key). if it can't figure out it will throw
# recommended pattern is to avoid this and use explicit join
rows = session.query(User, Address).join(Address).all()
for row in rows:
    print(row)

# filtering
row = session.query(User.name).join(User.addresses).filter(Address.email == "matus@woho.com").first()
print(row)

# join from right entity using select_from()
rows = session.query(User, Address).select_from(Address).join(Address.user).all();
for row in rows:
    print(row)

# join with *subquery*
# subquery returns "alias" construct for us to use
from sqlalchemy import func

# subquery is selectable unit, acts like a table (metadata)
subq = session.query( func.count(Address.id).label("count"), User.id.label("user_id") ).\
    join(Address.user).\
    group_by(User.id).\
    subquery()

rows = session.query(User.name, func.coalesce(subq.c.count, 0)).\
    outerjoin(subq, User.id == subq.c.user_id).all()

for row in rows:
    print(row)

print(subq)
print(subq.element)
print(subq.element.froms)
print(repr(subq.element.froms[0].left))
print(repr(subq.element.froms[0].right))
