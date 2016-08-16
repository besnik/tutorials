# define metadata for table

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

# JOIN
joinsql = user_table.join(city_table, user_table.c.city_id == city_table.c.id)
print(joinsql)  # "user" JOIN city ON "user".city_id = city.id

# JOIN on clausule figured out automatically
joinsql = user_table.join(city_table)
print(joinsql)  # "user" JOIN city ON city.id = "user".city_id

# SELECT * from JOIN
from sqlalchemy import select
sql = select([user_table, city_table]).select_from(joinsql)
print(engine.execute(sql).fetchall())

# SELECT col1, col2 from JOIN
sql = select([user_table.c.name, city_table.c.name]).select_from(joinsql)
print(engine.execute(sql).fetchall())


# SELECT number of people living per city_table, JOIN, SUB-SELECT, GROUP BY, ORDER BY
from sqlalchemy import func
print("---------------")

# city id + count(people)
sqlcitycount = select([user_table.c.city_id, func.count(1).label("count")]).\
    group_by(user_table.c.city_id).\
    alias();
print(engine.execute(sqlcitycount).fetchall()) # [(1, 1), (2, 2), (3, 1)]

# use join to link alias with another select
sqljoin = city_table.join(sqlcitycount, city_table.c.id == sqlcitycount.c.city_id)
sqlcityname_plus_count = select([city_table.c.name, sqlcitycount.c.count]).select_from(sqljoin).order_by(sqlcitycount.c.count)
print(engine.execute(sqlcityname_plus_count).fetchall()) # [('presov', 1), ('bratislava', 2), ('kosice', 1)]


