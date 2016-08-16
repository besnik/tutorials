# a scalar select returns exactly one row and one column

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String

metadata = MetaData() # metadata is collection of tables and can be traversed like XML DOM

city_table = Table("city", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    )

user_table = Table("user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    #Column("city_id", Integer, ForeignKey("city.id"))              # foreign key can be string "table.column"
    Column("city_id", Integer, ForeignKey(city_table.columns.id), nullable=False)   # or it can be reference of column object
    )


# init engine over database
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)

# create table from metadata
metadata.create_all(engine)

# insert data
result = engine.execute(city_table.insert(), [{"name":"presov"}, {"name":"bratislava"}, {"name":"kosice"}])
result = engine.execute(user_table.insert(), [{"name":"slavo", "city_id": 1}, {"name":"filip", "city_id": 2}, {"name":"berty", "city_id": 3}, {"name":"miska", "city_id": 2}])


# scalar select
from sqlalchemy import select, func

sqlcount = select([func.count(user_table.c.id)]).where(city_table.c.id == user_table.c.city_id)
print(engine.execute(sqlcount).fetchall()) # [(4,)]

sql = select([city_table.c.name, sqlcount.as_scalar()]);
print(engine.execute(sql).fetchall()) # [('presov', 1), ('bratislava', 2), ('kosice', 1)]