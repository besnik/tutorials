from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String

metadata = MetaData() # metadata is collection of tables

user_table = Table("user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
    )

# user_table (type of Table) is like XML DOM object - you can inspect individual elements
print(user_table.name);                     # user
print(user_table.columns.keys())            # ['id', 'name']
print(user_table.c)                         # ['user.id', 'user.name']
print(user_table.c.keys())                  # ['id', 'name']
print(repr(user_table.columns.id))          # Column('id', Integer(), table=<user>, primary_key=True, nullable=False)
print(repr(user_table.columns.name))        # Column('name', String(), table=<user>)
print(repr(user_table.columns.name.type))   # String()
print(repr(user_table))                     # Table('user', MetaData(bind=None), Column('id', Integer(), table=<user>, primary_key=True, nullable=False), Column('name', String(), table=<user>), schema=None)
print(repr(user_table.columns.name.table))  # Table('user', MetaData(bind=None), Column('id', Integer(), table=<user>, primary_key=True, nullable=False), Column('name', String(), table=<user>), schema=None)
print(repr(user_table.primary_key))         # PrimaryKeyConstraint(Column('id', Integer(), table=<user>, primary_key=True, nullable=False))

print(user_table.select())                  # SELECT "user".id, "user".name FROM "user"

print("done")


