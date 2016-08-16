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