from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:", echo=True)

# create table (connectionless execution via engine)
engine.execute("""CREATE TABLE emp (
id INTEGER PRIMARY KEY,
name VARCHAR(50)
)""")


# insert data as one explicit transaction
conn = engine.connect(); # get connection from pool
tnx = conn.begin(); # open transaction

# explicit execution (via connection)
conn.execute("INSERT INTO emp (name) VALUES (:name)", name="Slavo")
conn.execute("INSERT INTO emp (name) VALUES (:name)", name="Jano")
conn.execute("INSERT INTO emp (name) VALUES (:name)", name="Vlado")

tnx.commit(); # commit transaction
conn.close(); # return connection back to pool


# insert data as one explicit transaction using with statement with auto commit
with engine.begin() as conn:
    conn.execute("INSERT INTO emp (name) VALUES (:name)", name="Peter")
    conn.execute("INSERT INTO emp (name) VALUES (:name)", name="Matus")
    conn.execute("INSERT INTO emp (name) VALUES (:name)", name="Stano")


# query data
conn = engine.connect();
result = conn.execute("select id, name from emp")
conn.close();

for row in result:
    print("DATA: " + repr(row))