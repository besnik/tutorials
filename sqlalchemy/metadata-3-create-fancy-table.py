# define metadata for table

from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Numeric, Enum

metadata = MetaData() # metadata is collection of tables and can be traversed like XML DOM

fancy_table = Table("fancy", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("timestamp", DateTime),
    Column("money", Numeric(10,2)),
    Column("type", Enum("eur", "gbp", "usd")) # creates constraint in db: CHECK (type IN ('eur', 'gbp', 'usd'))
    )

# init engine over database
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)

# create table from metadata
metadata.create_all(engine)