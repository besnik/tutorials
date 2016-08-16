# define metadata for table

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy import Integer, Unicode, UnicodeText

metadata = MetaData() # metadata is collection of tables and can be traversed like XML DOM

city_table = Table("city", metadata,
    Column("id", Integer, primary_key=True),
    Column("version", Integer, primary_key=True),
    Column("name", UnicodeText)
    )

user_table = Table("user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Unicode(100)),
    Column("city_id", Integer),
    Column("city_version", Integer),
    ForeignKeyConstraint(
        ["city_id", "city_version"],
        ["city.id", "city.name"])
    )


# init engine over database
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)

# create table from metadata
metadata.create_all(engine)