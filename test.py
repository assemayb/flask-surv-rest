# person = {"name":"ahmed", "age": 19}
# name, age = person.get("name"), person.get("ssfa")
# print(name, age)

# if person.get('ass') is KeyError():
#     x = None
# if x == None:
#     print("nothing")
# else:
#     print(x)

class User(object):
    def __init__(self):
        self.id = 1
        self.name = "ass"

    def __repr__(self):
        return f"{self.name}{self.id}"

class SubUser(User):
    def __repr__(self):
        return f"{self.name}{self.id}"

u1 = SubUser()
print(u1.__class__())
