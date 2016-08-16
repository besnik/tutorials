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

# create table from metadata
metadata.create_all(engine)

# now load metadata for the table from database
metadata2 = MetaData();
user_table_reflected = Table("user", metadata2, autoload=True, autoload_with=engine);

print("-- TABLE SCHEMA LOADED FROM DB ---------------------")
print(repr(user_table_reflected))