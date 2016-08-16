# SQL Expressions system builds upon Table Metadata in order to compose SQL statemetns in Python
# We will build Python objects that represent individual SQL strings (statements) we'd send to the db
# Converted to strings when we "Execute" them (as well as if we print them)

# define metadata for table

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

print(user_table.c.name)    # user.name

# sql alchemy overloads operators like ==, > by implementing __eq__ method for many objects including Column
# as result of such expression is new sqlalchemy expr object (not true or false as you would expect)
x = user_table.c.name == "xy"
print(repr(x)) # <sqlalchemy.sql.elements.BinaryExpression object at 0x02CD51B0>

# get class tree of the expression
print(repr(type(x).__mro__)) 
"""
(<class 'sqlalchemy.sql.elements.BinaryExpression'>, 
<class 'sqlalchemy.sql.elements.ColumnElement'>, 
<class 'sqlalchemy.sql.operators.ColumnOperators'>, 
<class 'sqlalchemy.sql.operators.Operators'>, 
<class 'sqlalchemy.sql.elements.ClauseElement'>, 
<class 'sqlalchemy.sql.visitors.Visitable'>, 
<class 'object'>)
"""

# expressions become sql when evaluated as a String
# bound parameters are used. values are hidden to avoid sql injection problem
print(str(user_table.c.name == "xy"))                               # "user".name = :name_1
print((user_table.c.name == "xy") | (user_table.c.name == "zw"))    # "user".name = :name_1 OR "user".name = :name_2
print(user_table.c.id > 5)                                          # "user".id > :id_1
print(user_table.c.name == None)                                    # "user".name IS NULL
print(user_table.c.name != None)                                    # "user".name IS NOT NULL
print(user_table.c.name.is_(None))                                  # "user".name IS NULL

# number => addition
print(user_table.c.id + 5)                                          # "user".id + :id_1

# string => concatenation
print(user_table.c.name + "test")                                   # "user".name || :name_1

# OR and AND are available with | and &, or_(), and_()
from sqlalchemy import and_, or_

# 3 column comparisons embedded in 2 conjuction functions
print(
    and_(
        user_table.c.id == 1,
        or_(user_table.c.name == "xy", user_table.c.name == "zw")
    )
)
# "user".id = :id_1 AND ("user".name = :name_1 OR "user".name = :name_2)

# IN
print(user_table.c.name.in_(["slavo", "jano", "peter"]))    # "user".name IN (:name_1, :name_2, :name_3)

# Compile expression against different dialects (mysql vs oracle)
expr = user_table.c.name == "slavo"

# sqlite
print("sqlite sql statement: " + str(expr)) # have to type explicitely to str because + operator is overloaded for expressions
print("sqlite sql statement: " + str(expr.compile())) # explicit compiling

# mysql
from sqlalchemy.dialects import mysql
print("mysql sql statement: " + str(expr.compile(dialect=mysql.dialect())))     # user.name = %s

# oracle
from sqlalchemy.dialects import oracle
print("oracle sql statement: " + str(expr.compile(dialect=oracle.dialect())))   # "user".name = :name_1


# expression left and right parameters
print(repr(expr.left))
print(repr(expr.right))
print(repr(expr.operator))  # native python build-in function. example: import operator; operation.eq(x,y)


# compiled object
comp = expr.compile();

# get parameters of compiled expression (in expression it self the param was replaced by bound params :name_1)
print(comp.params)  # {'name_1': 'slavo'}

result = engine.execute(user_table.select().where(user_table.c.name == "slavo"))


