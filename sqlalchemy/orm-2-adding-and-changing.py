from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Base
Base = declarative_base() 

# Concrete type
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return "<User(id: %r, name: %r)>" % (self.id, self.name)

# Engine and create tables
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

# Session with identity map
from sqlalchemy.orm import Session
session = Session(bind=engine)

# adding single object as *pending*
u1 = User(name="slavo")
session.add(u1)
# execute query -> before execution *pending* objects are *flushed* to the db
s = session.query(User).filter_by(name="slavo").first();

# adding multiple objects as *pending*
session.add_all([
    User(name="jano"),
    User(name="vlado"),
    User(name="peter")
])

print(session.new)      # # IdentitySet([<User(id: None, name: 'peter')>, <User(id: None, name: 'jano')>, <User(id: None, name: 'vlado')>])

# modify persisted object - it is now marked as *dirty*
u1.name = "slafco" 

print(session.new)      # IdentitySet([<User(id: None, name: 'peter')>, <User(id: None, name: 'jano')>, <User(id: None, name: 'vlado')>])
print(session.dirty)    # IdentitySet([<User(id: 1, name: 'slafco')>])
print(u1.__dict__)      # {'name': 'slafco', 'id': 1, '_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x02E94650>}

# Commit always triggers a final *flush* of remainig changes and *ends transaction*
session.commit();

print(session.new)      # IdentitySet([])
print(session.dirty)    # IdentitySet([])
print(u1.__dict__)      # {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x02E94650>}

# After commit theres no transaction. The session invalidates all data, so that accessing them will automatically
# start a *new* transaction and re-load from the database.
# SQLalchemy it knows nothing about data if there is no transaction present.

print(u1.name) # causes opening *new transaction* and sql select
print(u1.__dict__)

u1.name = "slavomir" # dirty state
session.flush() # writes changes to the database without stopping transaction





