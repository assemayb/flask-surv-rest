import random


# for i in range(random.randint(0, 10)):
#     # print(i)
#     # print(random.randint(1, 5))


#     print(random.randint(1, 5))
#     print(random.randrange(1, 5))

# print(random.random())
# print(random.choice([x for x in range(random.randrange(1, 10000))]))
arr = [i for i in range(50)]
# print(random.sample(arr, 10))
# print(random.choice(arr))
random.shuffle(arr)
arr2 = arr
# print(arr2)

# print(chr(65 - 28))
# print(ord("A") - ord("a"))

def random_token_generator():
    token = ""
    all_small_letters = [chr(i) for i in range(97, 123)]
    nums = [str(i) for i in range(10)]
    chars = [str(i) for i in range(10) if i % random.randint(2, 5) == 0]
    for i in range(6):
        num = random.choice(nums)
        letter = random.choice(all_small_letters)
        char = random.choice(chars)
        token += num + letter + char
    return token

print(random_token_generator())