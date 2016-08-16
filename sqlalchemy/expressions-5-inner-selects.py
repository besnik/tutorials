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

# insert data in batch variant
sql = user_table.insert().values([{"name":"peter"}, {"name":"filip"}, {"name":"slavo"}, {"name":"jano"}, {"name":"filip"}])
conn = engine.connect()
result = conn.execute(sql)
conn.close();

# SELECT inside SELECT
from sqlalchemy import select
inner_select = select([user_table]).where(user_table.c.name == "filip")
outer_select = select([inner_select.c.name]).where(inner_select.c.id == 2) # select() object is "selectable" like table

print(engine.execute(outer_select).fetchall())

# Aliased (inner) SELECT inside (outer) SELECT
from sqlalchemy import select
inner_select = select([user_table]).where(user_table.c.name == "filip").alias()
outer_select = select([inner_select.c.name]).where(inner_select.c.id == 2) # select() object is "selectable" like table

print(engine.execute(outer_select).fetchall())