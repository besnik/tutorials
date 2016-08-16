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

# insert data
sql = user_table.insert().values(name = "slavo")
conn = engine.connect();
result = conn.execute(sql);
conn.close();

# insert data in batch
conn = engine.connect();
result = conn.execute(user_table.insert(), [{"name":"jano"}, {"name":"stano"}])
conn.close();

# insert data in batch variant
sql = user_table.insert().values([{"name":"peter"}, {"name":"filip"}])
conn = engine.connect();
result = conn.execute(sql);
conn.close();

