# define metadata for table

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String

metadata = MetaData() # metadata is collection of tables and can be traversed like XML DOM

city_table = Table("city", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    )

user_table = Table("user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    #Column("city_id", Integer, ForeignKey("city.id"))              # foreign key can be string "table.column"
    Column("city_id", Integer, ForeignKey(city_table.columns.id))   # or it can be reference of column object
    )


# init engine over database
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)

# create table from metadata
metadata.create_all(engine)


# init inspector
from sqlalchemy import inspect
inspector = inspect(engine)
print("--- Inspector loaded ---")

# get info about tables in database
print(inspector.get_table_names())          # ['user']
print(inspector.get_columns("user"))        # [{'type': INTEGER(), 'autoincrement': True, 'nullable': False, 'default': None, 'name': 'id', 'primary_key': 1}, {'type': VARCHAR(), 'autoincrement': True, 'nullable': True, 'default': None, 'name': 'name', 'primary_key': 0}]
print(inspector.get_foreign_keys("user"))   # [{'name': None, 'referred_columns': ['id'], 'referred_table': 'city', 'referred_schema': None, 'constrained_columns': ['city_id']}]

print("--- Find tables with column named city_id ---")
for tname in inspector.get_table_names():
    for column in inspector.get_columns(tname):
        if (column["name"] == "city_id"):
            print(tname)

