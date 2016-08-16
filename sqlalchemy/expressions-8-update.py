from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String

metadata = MetaData() # metadata is collection of tables and can be traversed like XML DOM

user_table = Table("user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
    )


# init engine over database
from sqlalchemy import create_engine, select
engine = create_engine("sqlite://", echo=True)

# create all tables from metadata
metadata.create_all(engine)

# insert data in batch variant
sql = user_table.insert().values([{"name":"peter"}, {"name":"filip"}, {"name":"slavo"}, {"name":"jano"}, {"name":"filip"}])
conn = engine.connect()
result = conn.execute(sql)
conn.close();


# UPDATE
sql = user_table.update().\
    values(name="jozo").\
    where(user_table.c.id == 2)

engine.execute(sql);

# SELECT
result = engine.execute(select([user_table]))
for row in result:
    print(row)


# UPDATE with expression
sql = user_table.update().\
    values(name=user_table.c.name + " the great").\
    where(user_table.c.id == 2)

engine.execute(sql);

# SELECT
result = engine.execute(select([user_table]))
for row in result:
    print(row)