# Example of reference variables, equation and object comparison

# both sasa and alex variables are referencing same object in memory (on the same address)
sasa = { "name": "sasa" } # lets create dictionary in memory and set sasa as variable pointing to it
alex = sasa; # sasa and alex are aliases to the same object in memory

print(sasa is alex)         # True

print(id(sasa))             # 5978072
print(id(alex))             # 5978072

sasa["age"] = 18            # modifying object sasa and alex are pointing to
print(alex)                 # {'name': 'sasa', 'age': 18}


# fake person is new object in memory with new address. it has same content as sasa/alex
fake_person = { 'name': "sasa", "age": 18 }    
print(id(fake_person))      # 4929576

# comparisons
print(fake_person is sasa)  # False
print(fake_person is alex)  # False

print(fake_person == sasa)  # True (because it compares values using __eq__ method of dictionary and not object IDs in memory)
print(fake_person == alex)  # True (because it compares values using __eq__ method of dictionary and not object IDs in memory)


# single types like int, str, byte, array.array are value types - they don't contain references
a = 1
b = a

a = 2
print(b)    # 1