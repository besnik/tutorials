# ----------
# dictionary
# ----------
person = {"name": "juraj", "fav_movie": "starwars"}
print(type(person))         # <class 'dict'>

print(person["name"])       # reading

person["age"] = 18          # writing
print(person)

print(len(person))          # 3 (number of properties)

# ---------
# list
# ---------
a = [1,2,3,4]
print(type(a))              # <class 'list'>
print(a[0])                 # 1 (zero indexed)
print(len(a))               # 4

b = [5,6,7]
c = a + b                   # concatenation
print(b)                    # [5, 6, 7]
print(c)                    # [1, 2, 3, 4, 5, 6, 7]

d = [i for i in range(10)]
print(type(d))              # <class 'list'>
print(d)                    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

d.append(10)                
print(d)                    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

i = d.pop()
print(i)                    # 10
print(d)                    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

i = d.pop(2)                
print(i)                    # 2
print(d)                    # [0, 1, 3, 4, 5, 6, 7, 8, 9]

d.remove(1)                 # removes first item whose value is 1
print(d)                    # [0, 3, 4, 5, 6, 7, 8, 9]

del d[0]
print(d)                    # [3, 4, 5, 6, 7, 8, 9]

del d[1:5]
print(d)                    # [3, 8, 9]

d.append(["slavo"])

d2 = list(d)                # copies are shallow by default
print(d2)                   # [3, 8, 9]
print(d==d2)                # True
print(d is d2)              # False

d3 = d[:]                   # copies are shallow by default
print(d3)                   # [3, 8, 9]
print(d==d3)                # True
print(d is d3)              # False

d3[3].append("jano")        # modifying object that is also referenced by d
print(d)                    # [3, 8, 9, ['slavo', 'jano']]
print(d3)                   # [3, 8, 9, ['slavo', 'jano']]
print(d==d3)                # True
print(d is d3)              # False

# deep copy
from copy import deepcopy
d4 = deepcopy(d3)
print(d4)                   # [3, 8, 9, ['slavo', 'jano']]
print(d3==d4)               # True
print(d3 is d4)             # False

d4[3].append("vlado")       # d4 contains deep copy of objects that are now separated in memory
print(d3)                   # [3, 8, 9, ['slavo', 'jano']]
print(d4)                   # [3, 8, 9, ['slavo', 'jano', 'vlado']]

# ----------
# tuples
# ----------
t1 = 1,2,3
print(type(t1))              # <class 'tuple'>
print(t1)                    # (1, 2, 3)

t2 = "slavo", "juro"
print(t2)                   # ('slavo', 'juro')

t3 = t1, t2
print(t3)                   # ((1, 2, 3), ('slavo', 'juro'))
print(t3[1][1])             # juro

try:
    t1[0] = 5 # touples are immutable
except Exception as e:
    print("Can not change touple! " + repr(e))

# but if touple stores mutable object then content of the mutable object can change
t = {"name": "slavo"}, 2,3,4
print(t)                    # ({'name': 'slavo'}, 2, 3, 4)
t[0]["name"] = "peter"
print(t)                    # ({'name': 'peter'}, 2, 3, 4)

# ------------
# named tuples
# ------------
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y']) # field names as sequence of strings

p = Point(1,2)
print(type(p))              # <class '__main__.Point'>
print(p)                    # Point(x=1, y=2)

x,y = p                     # unpacking

print(p.x)                  # 1 (accessible by name)
print(p[0])                 # 1 (accessible by index)


Point2 = namedtuple('Point2', "x y")    # field names separated by whitespace
p2 = Point2(y=4, x=3)
print(p2)

# ----------
# arrays
# ----------
# https://docs.python.org/3/library/array.html
# Arrays are sequence types and behave very much like lists, 
# except that the type of objects stored in them is constrained (chars, int, float)
from array import array
a1 = array("l", [1,2,3,4,5])
a2 = array("d", [1.0, 2.1, 3.14])

print(type(a1))             # <class 'array.array'>
print(a1)                   # array('l', [1, 2, 3, 4, 5])