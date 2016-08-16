# define metadata for table

from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String

metadata = MetaData() # metadata is collection of tables and can be traversed like XML DOM

user_table = Table("user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
    )


# init engine over database
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)

# create all tables from metadata
metadata.create_all(engine)

# creates single table
user_table.create(engine, checkfirst=True)

# drops single Table
user_table.drop(engine, checkfirst=True)

# drops all tables
metadata.drop_all(engine, checkfirst=True)