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

# column definition of object property
print(repr(User.name.property.columns[0])) # Column('name', String(), table=<user>)

# properties of mapped class act like Column objects and produce SQL expressions
print(User.name == "slavo") # "user".name = :name_1

# it is possible to use lower level access to the data using SQL expressions and connection+execute methods
# because properties of mapped class with properties acts like Table and Columns
from sqlalchemy import select
sql = select([User.id, User.name]).\
        where(User.name == "slavo").\
        order_by(User.id)

print(sql)

# engine level execution
rows = session.connection().execute(sql).fetchall();
for row in rows:
    print(row) # (1, 'slavo')

# orm execution
query = session.query(User).filter(User.name == "slavo").order_by(User.id)
rows = query.all();
for row in rows:
    print(row) # <User(id: 1, name: 'slavo')>

# Query returns individual columns
for id, name in session.query(User.id, User.name):
    print(id, name) # touple (1 slavo)

# Mix entities and columns together (if you want to join multiple tables...)
for row in session.query(User, User.name):
    print(row.User, row.name) # touple (<User(id: 1, name: 'slavo')> slavo)

# Array like access (will use Offset and Limit sql statements)
u = session.query(User).order_by(User.id)[2]
print(u)

# Array slices (will use Offset and Limit sql statements)
for u in session.query(User).order_by(User.id)[1:3]:
    print(u)

# WHERE using filter_by(keywords) - quick and simple
for user in session.query(User).filter_by(name="slavo"):
    print(user)

# WHERE using filter(sql expression) - flexible
for user in session.query(User).filter(User.name=="slavo"):
    print(user)

# conjunctions - OR
from sqlalchemy import or_
for user in session.query(User).filter(
    or_(User.name=="slavo", User.id < 5)
):
    print(user)

# conjuctions - AND
# Multiple filters join by AND just like select().where()
for user in session.query(User).\
    filter(User.name == "slavo").\
    filter(User.id < 5):
    print(user)

# Returning data - ALL
query = session.query(User);
print(query.all())

# Returning data - First
query = session.query(User);
print(query.first())

# Returning data - One
# checks if there is exactly one row returned, otherwise throws exception (no rows or multiple rows)
query = session.query(User).filter(User.name == "slavo")
print(query.one())

# creating queries from queries
q1 = session.query(User)
print(q1)
q2 = q1.filter(User.name == "slavo")
print(q2)