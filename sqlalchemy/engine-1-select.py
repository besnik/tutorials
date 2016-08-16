from sqlalchemy import create_engine

#engine = create_engine("sqlite:///some.db") # create sqlite db. use "////" to specify absolute path
engine = create_engine("sqlite:///:memory:", echo=True)

# create table
engine.execute("""CREATE TABLE emp (
id INTEGER PRIMARY KEY,
name VARCHAR(50)
)""")

# insert data (connectionless execution (via engine))
engine.execute("INSERT INTO emp (name) VALUES (:name)", name="Slavo")
engine.execute("INSERT INTO emp (name) VALUES (:name)", name="Jano")
engine.execute("INSERT INTO emp (name) VALUES (:name)", name="Vlado")

# query data
result = engine.execute("select id, name from emp")
rows = result.fetchall()
result.close(); # should be done automatically

# display data
for row in rows: # we could also iterate directly over result without need to call fetchall()
    print("DATA: " + repr(row))

print("done")

