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

# SELECT + WHERE
from sqlalchemy import select
sql = select([user_table.c.id, user_table.c.name]).\
    where(user_table.c.name == "filip")

conn = engine.connect()
result = conn.execute(sql)
conn.close()

for row in result:
    print(row)

# SELECT *
sql = select([user_table])
result = engine.execute(sql) # automatically handles connections

for row in result:
    print(row)

# SELECT *
sql = select([user_table])
result = engine.execute(sql).fetchall() # automatically handles connections

for row in result:
    print(row)


# SELECT * WHERE
from sqlalchemy import or_
sql = select([user_table]).\
    where(
        or_(user_table.c.name == "filip", user_table.c.name == "peter")
    )

engine.execute(sql).fetchall();

# SELECT multiple WHEREs, will be joined by and
sql = select([user_table]).\
    where(user_table.c.name == "filip").\
    where(user_table.c.name == "peter")

engine.execute(sql).fetchall();


# ORDER BY
sql = select([user_table]).\
    order_by(user_table.c.name)

print(engine.execute(sql).fetchall());