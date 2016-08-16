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
sql = user_table.insert().values([{"name":"jano"}, {"name":"filip"}, {"name":"slavo"}, {"name":"jano"}, {"name":"filip"}, {"name":"jano"}])
conn = engine.connect()
result = conn.execute(sql)
conn.close();

# selects count of names (+ order by count desc)
from sqlalchemy import func, select, desc
sql = select([user_table.c.name, func.count(1).label("count")]).\
    group_by(user_table.c.name).\
    order_by(desc("count"))

print(engine.execute(sql).fetchall())