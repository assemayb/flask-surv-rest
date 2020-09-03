import random


# for i in range(random.randint(0, 10)):
#     # print(i)
#     # print(random.randint(1, 5))


#     print(random.randint(1, 5))
#     print(random.randrange(1, 5))

# print(random.random())
# print(random.choice([x for x in range(random.randrange(1, 10000))]))
# arr = [i for i in range(50)]
# print(random.sample(arr, 10))
# print(random.choice(arr))
# random.shuffle(arr)
# arr2 = arr
# print(arr2)

# print(chr(65 - 28))
# # print(ord("A") - ord("a"))

# def random_token_generator():
#     token = ""
#     all_small_letters = [chr(i) for i in range(97, 123)]
#     nums = [str(i) for i in range(10)]
#     chars = [str(i) for i in range(10) if i % random.randint(2, 5) == 0]
#     for i in range(6):
#         num = random.choice(nums)
#         letter = random.choice(all_small_letters)
#         char = random.choice(chars)
#         token += num + letter + char
#     return token

# print(random_token_generator())


# my_list = [4, 7, 0, 3]
# my_iter = iter(my_list)
# print(next(my_iter))
# print(next(my_iter))
# print(my_iter.__next__())
# print(my_iter.__next__())

# iter_obj = iter(iterable)
# while True:
#     try:
#         elemet = next(iter_obj)
#     except StopIteration:
#         break

# class PowTwo:
#     def __init__(self, max=0):
#         self.max = max

#     def __iter__(self):
#         self.n = 0
#         return self

#     def __next__(self):
#         if self.n <= self.max:
#             result = 2 ** self.n
#             self.n += 1
#             return result
#         else:
#             raise StopIteration


# numbers = PowTwo(3)
# i = iter(numbers)
# print(next(i))
# print(next(i))
# print(next(i))
# print(next(i))
# print(next(i))

# print(next(x))
# print(next(x))


# my_list = [1, 3, 6, 10]
# 
# square each term using list comprehension
# list_ = [x**2 for x in my_list]

# same thing can be done using a generator expression
# generator expressions are surrounded by parenthesis ()
# generator = (x**2 for x in my_list)

# print(list_)
# x = next(generator)
# y = next(generator)
# for i in range(len(list_)):
#     print(next(generator))

lis = ["a", "b", "x"]
index = lis.index("a")
print(index)