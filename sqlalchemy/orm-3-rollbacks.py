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
    User(name="peter")
])

# finalize transaction
session.commit();
print('---transaction commited---')

# make changes again, add new object
u1.name = "slavomir" # dirty state
b = User(name="boris")
session.add(b) # pending state
print('---modifications done---')

# query flushes changes to the database; selects data from database. results come back
result = session.query(User).filter(User.name.in_(["slavomir", "boris"])).all()
print('---query done---')
print(result)


# rollback transaction to revert changes. change to u1 is reverted. boris is removed from db and session.
session.rollback();
print('---rollback done---')

print(u1) # causes *new transaction* to start and sql select. user has now original name before starting prev transaction.
print(b in session) # False (no sql call)

# boris does not exist in db since prev transaction was rolled back.
result = session.query(User).filter(User.name.in_(["slavo", "boris"])).all()
print('---query done---')
print(result)


